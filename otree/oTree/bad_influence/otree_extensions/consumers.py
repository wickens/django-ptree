import networkx as nx
from networkx.readwrite import json_graph
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer, WebsocketConsumer
import time
import json
from asgiref.sync import async_to_sync
from bad_influence.models import Player, Group, Constants


class NetworkVoting(WebsocketConsumer):

    def clean_kwargs(self):
        self.player_pk = self.scope['url_route']['kwargs']['player_pk']
        self.group_pk = self.scope['url_route']['kwargs']['group_pk']

    def connect(self):
        self.clean_kwargs()
        # self.player_pk = self.scope['url_route']['kwargs']['player_pk']
        # self.group_pk = self.scope['url_route']['kwargs']['group_pk']
        # Join
        self.channel_layer.group_add(
            self.connection_groups(),
            self.channel_name
        )

        self.accept()
        print("Connected to Network Socket")

    def disconnect(self, close_code):
        self.clean_kwargs()
        async_to_sync(self.channel_layer.group_discard)(
            self.connection_groups(),
            self.channel_name
        )
        print("Disconnected from Network Socket")

    def connection_groups(self, **kwargs):
        group_name = self.get_group().get_channel_group_name()
        personal_channel = self.get_player().get_personal_channel_name()
        return [group_name, personal_channel]

    def get_player(self):
        return Player.objects.get(pk=self.player_pk)

    def get_group(self):
        return Group.objects.get(pk=self.group_pk)

    def receive(self, text_data):
        self.clean_kwargs()
        text_data_json = json.loads(text_data)
        msg = text_data_json['message']
        player = self.get_player()
        group = self.get_group()

        if msg['action'] == 'guess' and msg['payload'] != Player.choice:
            new_guess = msg['payload']
            timestamp = time.time()

            subjective_time = msg['subjective_time'].split(":")
            if len(subjective_time) == 1:
                subjective_time = int(subjective_time[0]) * 60
            else:
                subjective_time = int(subjective_time[0]) * 60 + int(subjective_time[1])

            player.choice = new_guess
            player.last_choice_made_at = Constants.round_length - subjective_time
            player.save()

            graph = group.get_graph()
            consensus = group.get_consensus()

            group.add_to_history({
                "nodes": json_graph.node_link_data(graph)['nodes'],
                "minority_ratio": group.get_minority_ratio(),
                "time": timestamp,
                "choice": {
                    "id": player.id_in_group,
                    "value": player.choice,
                    "subjective_time": player.last_choice_made_at
                }
            })

            for p in group.get_players():
                ego_graph = json_graph.node_link_data(nx.ego_graph(graph, p.id_in_group))
                self.send(text_data=json.dumps({
                    'message': {
                        'ego_graph': ego_graph,
                        'consensus': consensus
                    }
                }))

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

        print("Sent message")


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        # self.player_pk = self.scope['url_route']['kwargs']['player_pk']
        self.group_pk = self.scope['url_route']['kwargs']['group_pk']
        self.room_name = 'chat_%s' % self.group_pk
        print("Player connected onto Chat Socket in group {}".format(self.group_pk))

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
        print('Disconnect from socket')

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        print('Received message')

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

        print("Sent message")
