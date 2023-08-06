import urllib
from os import environ

import pymongo
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from agents import NaiveAgent


SENDGRID_API_KEY = environ.get("SENDGRID_API_KEY")

# Should probably just be params to our model - passed when you commit to the
# back-end that is mongo.  This should cleanly extract into
MONGO_USERNAME = environ.get("MONGO_USERNAME")
MONGO_PASSWORD = environ.get("MONGO_PASSWORD")
MONGO_CLUSTER_URL = environ.get("MONGO_CLUSTER_URL")  # trailing slash?
MONGO_COLLECTION_NAME = environ.get("MONGO_COLLECTION_NAME") # collection for email records


class NaiveEmailApplication:
    """An application with the k-armed bandit as the decision model, the given Mongo table as the source of truth, and
    Sendgrid as the action medium.
    """
    def __init__(self):
        """Instantiate a NaiveEmailApplication.

        Creates an instance of a naive email application - parameterized bandits as implemented within curators
        through the agents.NaiveAgent model with abstracted interfaces with Mongo as the source of truth and sendgrid
        as the action medium.

        """
        mongo_client = pymongo.MongoClient(
            f"mongodb+srv://"
            f"{MONGO_USERNAME}:{urllib.parse.quote(MONGO_PASSWORD)}"
            f"@{MONGO_CLUSTER_URL}/")
        self.db = mongo_client.emailer

        # why maintaining state here and in mongo?
        self.email_variants = []
        self.outcomes = []


    def add_email_variant(self, variant_id, variant_name, variant_subject):
        """Add email variant to the list of available levers.

        Parameters
        ----------
        variant_id : str
            your variant id
        variant_name : str
            email variant name
        variant_subject : str
            subject for email variant
        """
        self.email_variants.append({"variant_subject": variant_subject,
                                    "variant_name": variant_name,
                                    "variant_id": variant_id})
        self.outcomes.append([1, 0])

    def send_message(self,
                     recipient_name,
                     recipient_email,
                     sender_email,
                     company):
        """Send an email.

        Parameters
        ----------
        recipient_name : str
            Name of recipient
        recipient_email : str
            Email address of recipient
        sender_email : str
            Email address to send from
        company : str
            Company

        """

        collection = self.db[MONGO_COLLECTION_NAME]


        message = Mail(from_email=sender_email,
                   to_emails=[recipient_email])

        # Choose best variant
        agent = NaiveAgent(
            target_var_type='rate',
            n_actions=len(self.outcomes),
            observations=self.outcomes,
        )
        selection = agent.sample(1)[0]
        recommendation = self.email_variants[selection]

        message.dynamic_template_data = {
                "subject": recommendation['variant_subject'],
                "name": recipient_name,
        }

        message.template_id = recommendation['variant_id']
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.headers.get_all('X-Message-Id')[0])
        email_details = {}
        email_details['company'] = company
        email_details['sender'] = sender_email
        email_details['email_address'] = recipient_email
        email_details['email_id'] = response.headers.get_all('X-Message-Id')[0]
        email_details['email_version_name'] = recommendation['variant_name']
        x = collection.insert_one(email_details)
        print("Email sent to: {}".format(recipient_email))

    def update_and_print_observations(self):
        """Reaches out to Mongo for responses and updates internal aggregates.  Prints retrieved stats.
        """

        # re-query your email data
        # probably don't need to re-connect to just re-query
        mongo_client = pymongo.MongoClient(
            f"mongodb+srv://"
            f"{MONGO_USERNAME}:{urllib.parse.quote(MONGO_PASSWORD)}"
            f"@{MONGO_CLUSTER_URL}/")
        db = mongo_client.emailer
        collection = db[MONGO_COLLECTION_NAME]

        # %%

        # Pull Mongo Records
        results = pd.DataFrame(list(collection.find()))
        # todo: change these prints either to logs or to explicit get functions
        print("Raw Mongo result head:")
        print(results.tail())

        print("Aggregate response from Mongo::")
        print(f"Samples -> {results.shape[0]}")
        print(f"Delivered -> {results['delivered'].sum()}")
        print(f"Opened -> {results['open'].sum()}")
        clicks = results.shape[0] - results['click'].isna().sum()
        print(f"Clicked -> {clicks}")
        print(f"CTR -> {(clicks / results.shape[0])}")

        # Update Outcome Probabilities

        for index, row in results.iterrows():
            for i, dic in enumerate(self.email_variants):
                if dic['variant_name'] == row['email_version_name']:
                    if row['click'] > 0:
                        self.outcomes[i][0] += 1

        print("Updated observations:")
        print(self.outcomes)
