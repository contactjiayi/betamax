# -*- coding: utf-8 -*-
from .base import BaseSerializer

import os


class SerializerProxy(BaseSerializer):

    """
    This is an internal implementation detail of the betamax library.

    No users implementing a serializer should be using this. Developers
    working on betamax need only understand that this handles the logic
    surrounding whether a cassette should be updated, overwritten, or created.

    It provides one consistent way for betamax to be confident in how it
    serializes the data it receives. It allows authors of Serializer classes
    to not have to duplicate how files are handled. It delegates the
    responsibility of actually serializing the data to those classes and
    handles the rest.

    """

    def __init__(self, serializer, cassette_path, allow_serialization=False):
        self.proxied_serializer = serializer
        self.allow_serialization = allow_serialization
        self.cassette_path = cassette_path

    def _ensure_path_exists(self):
        if not os.path.exists(self.cassette_path):
            open(self.cassette_path, 'w+').close()

    @staticmethod
    def generate_cassette_name(serializer, cassette_library_dir,
                               cassette_name):
        return serializer.generate_cassette_name(
            cassette_library_dir, cassette_name
            )

    def serialize(self, cassette_data):
        if not self.allow_serialization:
            return

        self._ensure_path_exists()

        with open(self.cassette_path, 'w') as fd:
            fd.write(self.proxied_serializer.serialize(cassette_data))

    def deserialize(self):
        self._ensure_path_exists()

        data = {}
        with open(self.cassette_path) as fd:
            data = self.proxied_serializer.deserialize(fd.read())

        return data