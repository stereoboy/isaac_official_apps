.. _cplusplus_ping:

Developing Codelets in C++
==========================

The goal of this tutorial is to develop a codelet in C++ that is effectively a machine that goes
"ping". For this tutorial, no external dependencies or special hardware is required.

Start by creating a new package by creating a folder in the isaac/packages directory with a command
similar to the following:

.. code-block:: python

   bob@desktop:~/isaac/packages/$ mkdir ping

For the rest of the tutorial whenever you are asked to create a new file place it directly into this
folder. More complicated packages will have subfolders but for this tutorial things are kept simple.

Every Isaac application is based on a JSON file. The JSON file describes the dependencies of the
application, the node graph and the message flow, and contains custom configuration. Create a new
JSON file called ``ping.app.json`` and specify its name as seen in the following snippet:

.. code-block:: python

  {
    "name": "ping"
  }

Next, create a bazel build file for compiling and running the application. Bazel provides very good
dependency management and excellent build speed for large projects, and bazel build files are very
easy to write. Create a file ``BUILD`` with a new app target with name ``ping``, as shown below:

.. code-block:: bash

    load("//engine/build:isaac.bzl", "isaac_app", "isaac_cc_module")

    isaac_app(
         name = "ping"
    )

Now you can build the application by running the following command in the ping directory. From now
on when you are asked to execute a command, execute it in the ping directory.

.. code-block:: bash

    bob@desktop:~/isaac/packages/ping$ bazel build ping

The command may take some time as all external dependencies of the Isaac Robot Engine are downloaded
and compiled. After a while the first build should have succeeded with output similar to the
following:

.. code-block:: bash

   bob@desktop:~/isaac/packages/ping$ bazel build ping
   Starting local Bazel server and connecting to it...
   INFO: Analysed target //packages/ping:ping (54 packages loaded, 2821 targets configured).
   INFO: Found 1 target...
   Target //packages/ping:ping up-to-date:
     bazel-genfiles/packages/ping/run_ping
     bazel-bin/ping/packages/ping
   INFO: Elapsed time: 112.170s, Critical Path: 30.14s, Remote (0.00% of the time):
   [queue: 0.00%, setup: 0.00%, process: 0.00%]
   INFO: 691 processes: 662 linux-sandbox, 29 local.
   INFO: Build completed successfully, 1187 total actions

Next you can run your new application by executing the following command:

.. code-block:: bash

   bob@desktop:~/isaac/packages/ping$ bazel run ping

This will start the ping application and keep it running. You can stop a running application by
pressing `Ctrl+C` in a console. This will gracefully shut down the application. You will notice
that not much is happening, because we don't have an application graph yet. Next we will create
some nodes for the application.

Creating a Node
----------------------

An Isaac application consists of many nodes running in parallel. They can send each other messages
or interact with each other using various other mechanisms provided by the Isaac Robot Engine. Nodes
are light-weight and do not require their own processes, or even their own threads.

To customize the behavior of the ping node, we have to equip it with components. We will create our
own component called ``Ping``. Create a new file ``Ping.hpp`` in the ``ping`` directory,
with the following contents:

.. code-block:: cpp

    #pragma once
    #include "engine/alice/alice_codelet.hpp"
    class Ping : public isaac::alice::Codelet {
     public:
      void start() override;
      void tick() override;
      void stop() override;
    };
    ISAAC_ALICE_REGISTER_CODELET(Ping);

Codelets provide three main functions which can be overloaded: ``start``, ``tick`` and ``stop``.
When a node is started the start functions of all attached codelets are called first.
For example, ``start`` is a good place to allocate resources. You can configure a codelet to ``tick``
periodically or each time a new message is received. Most of the functionality is then performed by
the ``tick`` function.

At the end when a node stops the ``stop`` function is called. You should free all previously
allocated resources in the ``stop`` function. Do not use constructors or destructors. You do not
have access to any of the Isaac Robot Engine functionality such as configuration in the constructor.

Each custom codelet you create needs to be registered with Isaac Robot Engine. This is done at the
end of the file using the ``ISAAC_ALICE_REGISTER_CODELET`` macro. In case your codelet is inside a
namespace you have to provide the fully qualified type name, for example
``ISAAC_ALICE_REGISTER_CODELET(foo::bar::MyCodelet)``.

To add some functionality to the codelet, create a source file called ``Ping.cpp`` which contains
this functionality:


.. code-block:: cpp

    #include "Ping.hpp"
    void Ping::start() {}
    void Ping::tick() {}
    void Ping::stop() {}

Codelets can tick in multiple different ways, but for now use periodic ticking. This can be achieved
by calling the ``tickPeriodically`` function in the codelet ``Ping::start`` function. Add the following
code to the ``start`` function in ``Ping.cpp``

.. code-block:: cpp

    void Ping::start() {
      tickPeriodically();
    }

To verify that something is in fact happening we print a message when the codelet ticks. The Isaac
SDK includes utility functions for logging data. LOG_INFO can be used to print a message on the
console. It follows the `printf-style syntax <https://en.cppreference.com/w/cpp/io/c/fprintf>`_. Add
the ``tick`` function to Ping.cpp as shown below:

.. code-block:: cpp

    void Ping::tick() {
      LOG_INFO("ping");
    }

Add a module to BUILD as shown below:

.. code-block:: python

    isaac_app(
      ...
    )

    isaac_cc_module(
      name = "ping_components",
      srcs = ["Ping.cpp"],
      hdrs = ["Ping.hpp"],
    )

An Isaac module defines a shared library that encapsulates a set of codelets and can be used by
different applications.

In order to use the Ping codelet in the application we first need to create a new node in the
application JSON file:

.. code-block:: python

    {
      "name": "ping",
      "graph": {
        "nodes": [
          {
            "name": "ping",
            "components": []
          }
        ],
        "edges": []
      }
    }

Each node can contain multiple components which define its functionality. Add the Ping codelet to
the node by adding a new section in the components array:

.. code-block:: python

    {
      "name": "ping",
      "graph": {
        "nodes": [
          {
            "name": "ping",
            "components": [
              {
                "name": "ping",
                "type": "Ping"
              }
             ]
          }
        ],
        "edges": []
      }
    }

An application graph normally has edges connecting different nodes, which determine the message
passing sequence between different nodes. Because this application does not have any other nodes,
leave the edges blank.

If you would try to run this application it would panic and show the error message
`Could not load component 'Ping'`. This happens because all components used in an applications
must be added to the modules list. You need to do this both in the BUILD file and in the application
JSON file:

.. code-block:: bash

    load("//engine/build:isaac.bzl", "isaac_app", "isaac_cc_module")

    isaac_app(
        name = "ping",
        modules = ["//packages/ping:ping_components"]
    )

.. code-block:: python

    {
      "name": "ping",
      "modules": [
        "ping:ping_components"
      ],
      "graph": {
        ...
      }
    }

Note that the expression `ping:ping_components` referes to the module
`//package/ping:ping_components` which we created previously.

If you would run the application now you would get a different panic message:
`Parameter 'ping/ping/tick_period' not found or wrong type`. This message appears because we need
to set the tick period of the Ping codelet in the configuration section. We will do this in the next
section.


Configuration
-------------

Most code requires various parameters for customizing behavior. For example, you might want to give
the user of our ping machine the option to change the tick period. In the Isaac framework this can
be achieved with configuration.

Let's specify the tick period in the configuration section of the application JSON file so that we
can finally run the application.

.. code-block:: python

    {
      "name": "ping",
      "modules": [
        "ping:ping_components"
      ],
      "graph": {
        ...
      },
      "config": {
        "ping" : {
          "ping" : {
            "tick_period" : "1Hz"
          }
        }
      }
    }

Every configuration parameter is referenced by three elements: node name, component name and
parameter name. In this case we are setting the parameter `tick_period` of the component `ping` in
the node `ping`.

Now the application will run successfully and will print "ping" once a second. You should see an
output similar to the snippet below. You can gracefully stop the application by pressing `Ctrl+C`.

.. code-block:: bash

    bob@desktop:~/isaac/packages/ping$ bazel run ping
    2019-03-24 17:09:39.726 DEBUG   engine/alice/backend/codelet_backend.cpp@61: Starting codelet 'ping/ping' ...
    2019-03-24 17:09:39.726 DEBUG   engine/alice/backend/codelet_backend.cpp@73: Starting codelet 'ping/ping' DONE
    2019-03-24 17:09:39.726 DEBUG   engine/alice/backend/codelet_backend.cpp@291: Starting job for codelet 'ping/ping'
    2019-03-24 17:09:39.726 INFO    packages/ping/Ping.cpp@8: ping
    2019-03-24 17:09:40.727 INFO    packages/ping/Ping.cpp@8: ping
    2019-03-24 17:09:41.726 INFO    packages/ping/Ping.cpp@8: ping

The `tick_period` parameter is automatically created for us, but we can also create our own
parameters to customize the behavior of codelets. Add a parameter to your codelet as shown below:

.. code-block:: cpp

   class Ping : public isaac::alice::Codelet {
    public:
     void start() override;
     void tick() override;
     void stop() override;
     ISAAC_PARAM(std::string, message, "Hello World!");
   };

``ISAAC_PARAM`` takes three arguments. First is the type of the parameter. Most often this is either
``double``, ``int``, ``bool``, or ``std::string``. The second argument is the name of our parameter.
The name is used to access or specify the parameter. The third argument is the default value to use
for this parameter. If there is no default value given and the parameter is not specified via a
configuration file, the program asserts when the parameter is accessed. The ``ISAAC_PARAM`` macro
creates an accessor called ``get_message`` and a bit more code to properly connect the parameter
with the rest of the system.

We can use the parameter now in the ``tick`` function instead of the hard-coded value:

.. code-block:: cpp

    void tick() {
      LOG_INFO(get_message().c_str());
    }

The next step is to add the configuration for the node. The config parameter uses node names,
component names, and the parameter name to specify desired values.

.. code-block:: python

    {
      "name": "ping",
      "modules": [
        "ping:ping_components"
      ],
      "graph": {
        ...
      },
      "config": {
        "ping" : {
          "ping" : {
            "message": "My own hello world!",
            "tick_period" : "1Hz"
          }
        }
      }
    }

That's it! You now have an application that can periodically print a custom message. Run the
application with the following command:

.. code-block:: bash

    bob@desktop:~/isaac/packages/ping$ bazel run ping

As expected, the codelet prints the message periodically on the command line.


Sending Messages
----------------

The custom codelet Ping is happily ticking. In order for other nodes to react to the ping, the
Ping codelet must send a message which other codelets can receive.

Publishing a message is easy. Use the ``ISAAC_PROTO_TX`` macro to specify that a codelet is
publishing a message. Add it to Ping.hpp as shown below:

.. code-block:: cpp

    #pragma once

    #include "engine/alice/alice.hpp"
    #include "messages/messages.hpp"

    class Ping : public isaac::alice::Codelet {
     public:
      ...

      ISAAC_PARAM(std::string, message, "Hello World!");
      ISAAC_PROTO_TX(PingProto, ping);
    };

   ISAAC_ALICE_REGISTER_CODELET(Ping);

The ``ISAAC_PROTO_TX`` macro takes two arguments. The first one specifies the message to publish.
Here, use the PingProto message which comes as part of the Isaac message API. Access PingProto by
including the corresponding header. The second argument specifies the name of the channel under
which we want to publish the message.

Next, change the ``tick`` function to publish a message instead of printing to the console. The
Isaac SDK currently supports `cap’n’proto <https://capnproto.org/>`__ messages. Protos are a
platform and language independent way of representing and serializing data. Creating a message is
initiated by calling the ``initProto`` function on the accessor which the ``ISAAC_PROTO_TX`` macro
created. This function returns a cap’n’proto builder object which can be used to write data
directly to the proto.

The ``ProtoPing`` message has a field called ``message`` of type string, so in this instance we can
use the ``setMessage`` function to write some text to the proto. After the proto is populated we can
send the message by calling the publish function. This immediately sends the message to any
connected receivers. Change the tick() function in Ping.cpp to the following:

.. code-block:: cpp

    ...
    void Ping::tick() {
      // create and publish a ping message
      auto proto = tx_ping().initProto();
      proto.setMessage(get_message());
      tx_ping().publish();
    }
    ...

Lastly, upgrade the node (in the JSON file) to support message passing. Nodes in the Isaac SDK are
by default light-weight objects requiring minimal setup of mandatory components. Not necessarily
every node in your applications publish or receive messages. To enable message passing on a node we
need to add a component called ``MessageLedger``. This component handles incoming and outgoing
messages and relays them to ``MessageLedger`` components in other nodes.

.. code-block:: python

    {
      "name": "ping",
      "graph": {
        "nodes": [
          {
            "name": "ping",
            "components": [
              {
                "name": "message_ledger",
                "type": "isaac::alice::MessageLedger"
              },
              {
                "name": "ping",
                "type": "Ping"
              }
             ]
          }
        ],
        "edges": []
    },
    "config": {
      ...
    }

Build and run the application. It appears that nothing happens, because right now nothing is
connected to your channel. While you are publishing a message, no one is there to receive it and
react to it. You will fix that in the next section.

Receiving Messages
------------------

You need a node which can receive the ping message and react to it in some way. For this purpose
let us create a ``Pong`` codelet which gets triggered by the message sent by ``Ping``. Create a new
file Pong.hpp with the following contents:


.. code-block:: cpp

    #pragma once
    #include "engine/alice/alice.hpp"
    #include "messages/messages.hpp"

    class Pong : public isaac::alice::Codelet {
     public:
      void start() override;
      void tick() override;

      // An incoming message channel on which we receive pings.
      ISAAC_PROTO_RX(PingProto, trigger);

      // Specifies how many times we print 'PONG' when we are triggered
      ISAAC_PARAM(int, count, 3);
    };

    ISAAC_ALICE_REGISTER_CODELET(Pong);

The ``Pong`` codelets need to be added to the `ping_components` module in order to be compiled. Add
it to the BUILD file as shown below:

.. code-block:: python

    isaac_cc_module(
      name = "ping_components",
      srcs = [
        "Ping.cpp",
        "Pong.cpp"
      ],
      hdrs = [
        "Ping.hpp",
        "Pong.hpp"
      ],
    )

In the application JSON, create a second node and attach the new Pong codelet to it.
Connect the Ping and the Pong nodes via the edges:

.. code-block:: python

  {
    "name": "ping",
    "modules": [
      "ping:ping_components"
    ],
    "graph": {
      "nodes": [
        {
          "name": "ping",
          "components": [
            {
              "name": "message_ledger",
              "type": "isaac::alice::MessageLedger"
            },
            {
              "name": "ping",
              "type": "Ping"
            }
          ]
        },
        {
          "name": "pong",
          "components": [
            {
              "name": "message_ledger",
              "type": "isaac::alice::MessageLedger"
            },
            {
              "name": "pong",
              "type": "Pong"
            }
          ]
        }
      ],
      "edges": [
        {
          "source": "ping/ping/ping",
          "target": "pong/pong/trigger"
        }
      ]
    },
    "config": {
      "ping" : {
        "ping" : {
          "message": "My own hello world!",
          "tick_period" : "1Hz"
        }
      }
    }
  }

Edges are connecting receiving RX channels to transmitting TX channels. A transmitting channel can
transmit data to multiple receivers. A receiving channel can also receive data from multiple
transmitters, however this comes with caveats and is discouraged. Similar to parameters, channels
are referenced by three elements: node name, component name and channel name. An edge can be created
by adding it to the "edges" section in the application JSON file. Here `source` is the full name of
the transmitting channel and `target` is the full name of the receiving channel.

The last remaining task is to set up the Pong codelet to do something when it receives the ping.
Create a new file Pong.cpp. Call the ``tickOnMessage`` function in ``start`` to instruct the codelet
to tick each time it receives a new message on that channel. In ``tick`` we add the functionality to
print out "PONG!" as many number of times as defined by the "count" parameter in Pong's header file:

.. code-block:: cpp

  #include "Pong.hpp"

  #include <cstdio>

  void Pong::start() {
    tickOnMessage(rx_trigger());
  }

  void Pong::tick() {
    // Parse the message we received
    auto proto = rx_trigger().getProto();
    const std::string message = proto.getMessage();

    // Print the desired number of 'PONG!' to the console
    const int num_beeps = get_count();
    std::printf("%s:", message.c_str());
    for (int i = 0; i < num_beeps; i++) {
      std::printf(" PONG!");
    }
    if (num_beeps > 0) {
      std::printf("\n");
    }
  }

By using ``tickOnMessage`` instead of ``tickPeriodically`` we instruct the codelet to only tick when
a new message is received on the incoming data channel, in this case `trigger`. The tick function
now only execute whenever you receive a new message. This is guaranteed by the Isaac Robot Engine.

Run the application. You should see how a "pong" is generated every time the Pong codelet receives a
ping message from the Ping codelet. By changing the parameters in the configuration file you can
change the interval at which a ping is created, change the message which is sent together with each
ping, and print pong more or less often whenever a ping is received.

This is just quick start with a very simple application. A real-world application consists of
dozens of nodes, each with multiple components and most with one or more codelets. Codelets receive
multiple types of messages, call specialized libraries to solve hard computational problems, and
publish their results again to be consumed by other nodes.
