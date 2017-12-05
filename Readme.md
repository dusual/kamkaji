### Yet another task queue? Why?

We at e2enetworks manage multiple services and manage infrastructures across multiple providers including our inhouse one. Although our app is written in python/django, we needed a task queue that could handle the heterogeneity of our system. Hence, we went with the system where the business intelligenece is mostly handled in the client. Beanstalkd seemed like nice work queue and our solution is written on top of that.


### Installation




### Usage

#### Running the worker

#### Adding jobs to the client



#### Reporting Backend



### Contributors

- Ashish Mukherjee
- Amit Sethi [@dusual](https://github.com/dusual)


### TODO and future:

- Better handling for retry
- Better handling for delayed jobs
- Suggestions??

