#ifndef BASE_SERVICE_HPP
#define BASE_SERVICE_HPP

#include <vector>
#include <fstream>

namespace Terminal {


/*
 * Generic base class to listen to add, update, and remove 
 * events on a service. This listener should be registered 
 * on a service for the service to notify all listeners for
 * these events 
 */
template<typename T>
class ServiceListener {

public: 

    // Listener callback to process an add event to the service
    virtual void add_process(T& data) = 0;

    // Listener callback to process a remove event to the Service
    virtual void ProcessRemove(V &data) = 0;

    // Listener callback to process an update event to the Service
    virtual void ProcessUpdate(V &data) = 0;

private:

};

/*
 * Generic base class service 
 */
template<typename T, typename V>
class Service {

public:

    // get data on a service given a key
    virtual V& get_data(T key) = 0;

    // callback that a connector should invoke for any new or updated data 
    virtual void on_message(V& data) = 0;

    // add a listener to the service for callbacks on add, remove, and update events 
    // for data to the Service.
    virtual void add_listener(ServiceListener<V>* listener) = 0;

    // get all listeners on a service
    virtual const vector<ServiceListener<V>* >& get_listeners() const = 0;


private:

};

/*
 * Generic conncetor class
 * Invokes the service.on_message() method for subscriber connectors to push data to the service
 * Service can invoke the publish() method on this service to publish data to the connector for a publisher connector
 * Connectors are: publisher-only, subscriber-only, or both
 */
template<typename V>
class Connector {

public:

    // publish data to connector
    virtual void publish(V& data) = 0;


private:


};



}

#endif 