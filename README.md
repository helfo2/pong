# Distributed Pong

Video: access the video (pt-br) demonstrating the game [here](https://youtu.be/u6hogayJ2PQ) 

## Pre-requisites

Distributed Pong works with the socket directive - purely sockets in Python 3.7+ - along with Pygame 1.9+ to draw objects in the display surface (game window). We have used threading in the server to execute each client instance and feed them with the game events.

## Files and code organization



## Summary
This  project implements a distributed Pong game. Pong was the first profitable videogame in history, released by Atari in 1972. It is a sports game in 2-dimensions simulating table tennis. The player controls a paddle (vertical bar) moving it vertically in the left side of the screen, and competes with the computer or other player which controls the second paddle in the opposite side. Both players use their paddles to hi the ball and send it to the other side of the table.

You will find code from scratch to deal with latency, collision detection in the graphics structure and game development logic to fullfill those requirements. 

## Features

The entire protocol developed for distributed Pong is based on the concept of state replication, very popular among today's online games (more about the theory [here](https://0fps.net/2014/02/10/replication-in-networked-games-overview-part-1/)). Basically, we have implemented the active state replication strategy, in which the server is responsible for knowing all variables and behaviors regarding the state of the gamee deliver copies of this state to each of the clients. This simplified our work, since through passive replication (another option to solve that) clients are responsible to update their neighbors in the topology, and more complexity would need to be put into each client connection.

That said, we can think of a star topology for distributed Pong, to which the server is a central point of processing (or possibly, failure). This apporach is also very popular in this kind of game because, besides the probability of errors or bottlenecks, it can be highly reduced through the use of clustering.

## Application protocol

Distributed Pong runs on top of TCP. That enables the server to be multithreaded easily given connections. On the other hand, this can add some latency on far-distant networks due to the overhead of 40 bytes from TCP header, against only 8 bytes in the case of if have chosen UDP. If the main use of this code is in controlled environments, this shouldn't be an issue.

To minimize bandwidht usage, distributed Pong utilizes the notion of types of messages, in a similiar manner to the one of ICMP. The packets are sent in binary format of the primitive data types encoded (via the Python struct module). This happens without the need of deserialization of dumps. That way it is possible to have complete control of how many bytes can travel through the network for each message.

## Message formats

Types of messages represent states of the distributed Pong game. There are 2 for mostly that (START, WAIT). There are also two more (POS, SCORE) for the real time events and a last one for initial state support (STATE), making it 5 different types. In terms of bytes, all messages begin with their type, an unsigned short with 2 bytes. That's how the protocol knows beforehand the begin and end of messages as bytestreams. About each message type:

***START (code 1)***

indicates the start of the game. Once the server sends it to both clients, game events start to be generated in the server and graphics are loaded in the clients. Has length of only 2 bytes, with the code itself;

***WAIT (code 2)***

waits for the beginning of the game. This solves synchronization between both players. The first connects with the server alone, waiting for the second for a pre-determined time (like 10 seconds). Consists of the type of message followed by the timeout, totalizing 6 bytes;

***POS (code 3)***

holds information from the ball and the paddles, as points P(float x, float y) of the upper left corner from each object. Is sent in real-time and possesses 2 floats, totalizing 10 bytes;

***SCORE (code 4)***

marks the scores, with two integers, for the points of the player on the left and right side. Also in real time. Has a length of 10 bytes;

***STATE (code 5)***

keeps information about the initial state of the game. For the first connected player, it must be WAITING (for it to wait for the second one) and for the second connected player, STARTING (so that the game can already be started). Used for synchronization. Total lenght of 4 bytes.

## How the game works

The server operates with two simultaneous clients, opening a thread for each plus a thread to generate game events, namely the positions of the ball, paddles and the global score. These informations are given from a producer to both consumer client threads. A thread-safe queue per client helps with that.

The consumer threads, then, send the data from events to each client through the network. Synchronized, they replicate the state of the game in each window. The sync happens across two basic events:


* only one connected client: waits for the next client a pre-defined time (10 seconds). In case there is no other connection and this wait times out, the game dies and it is mandatory to reset the server for a new game.

* two connected clients: the game ends whenever one of the players hit 15 points. The game runs throughout the threads mentioned above.

To play, it suffices to configure some server parameters in the file config.py, run the file server.py and, after that, run two game.py instances.

## Features that would be cool

* Support for more players
* An explicit RESET state, enabling the possibility of not being necessary to reset the server. 
* Maybe use of UDP protocol specially for real-time events, instead of TCP. This would avoid some overhead (20 bytes TCP header).
* AI
* Ball acceleration over time

Feel free to use the code and enjoy playing!

***Note that MACOSX systems may have an issue with SDL (on top of which pygame is developed). Make sure to use Python 3.7.2 and Pygame 1.9.2, because for newer versions this could make the screen blank - [see this issue](https://github.com/pygame/pygame/issues/555)***
