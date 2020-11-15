#!/bin/python
import os
from flask_restful import Resource, reqparse
import psycopg2
import urllib.parse


DATABASE_URL = os.environ['DATABASE_URL']
cnx = psycopg2.connect(DATABASE_URL, sslmode='require')
parser = reqparse.RequestParser()


class Database(Resource):
    def get(self, name):
        cursor = cnx.cursor()
        select_meme = ("Select link "
                       "FROM memes "
                       "WHERE name = %s")
        cursor.execute(select_meme, (name,))
        cnx.commit()
        for link in cursor:
            imageurl = link[0]
        if imageurl != "":
            return {"name": name, "link": imageurl}, 200
        return "Link not found", 404


class Add(Resource):
    def post(self):
        parser.add_argument('name', type=str)
        parser.add_argument('link', type=str)
        parser.add_argument('description', type=str)
        args = parser.parse_args()
        cursor = cnx.cursor()
        add_meme = ("INSERT INTO memes "
                    "(name, link, describe) "
                    "Values (%s,%s,%s)")
        varis = (args['name'], args['link'], args['description'])
        cursor.execute(add_meme, varis)
        cnx.commit()
        return {"confirmation": "{} added successfully".format(args['name'])}, 201

    def put(self):
        parser.add_argument('name', type=str)
        parser.add_argument('link', type=str)
        args = parser.parse_args()
        cursor = cnx.cursor()
        edit_meme = ("UPDATE memes "
                     "SET link=%s "
                     "WHERE name=%s")
        varis = (args['link'], args['name'])
        cursor.execute(edit_meme,varis)
        cnx.commit()
        return {"Confirmation": "{}'s link edited successfully".format(args['name'])}, 202



