from django.test import TestCase

# Create your tests here.
import json
from .models import Client
from datetime import datetime
import requests
from django.core.files import File
from io import BytesIO


def add_clients():
    file = open("clients_data/3760-4000.json", "r", encoding="utf-8")
    data = json.load(file)
    for client in data:
        try:
            if client.get("photo"):
                response = requests.get(client.get("photo"))
                if response.status_code == 200:
                    img_data = response.content
                    img_file = BytesIO(img_data)

                    file_name = client.get("photo").split("/")[-1]
                    file_extension = file_name.split(".")[-1]

                    c = Client.objects.get(id=client['id'])
                    c.photo.save(f"photo_{c.id}.{file_extension}", File(img_file), save=True)
                    c.save()

        except Client.DoesNotExist:
            print("Client doesn't exist")
            Client.objects.create(id=client['id'], name=client['name'], address=client['address'],
                                  phone=client['phone'],
                                  birth_date=datetime.strptime(client["birth_date"], "%Y-%m-%d").date())
            print(f"Client {client['id']} created!")


def mobiles():
    count = 0
    for client in Client.objects.all():
        phone = client.phone
        duplicates = Client.objects.filter(phone=phone).count()
        if duplicates > 1:
            print(phone, client.id, duplicates)
            count += 1
    print(count)
