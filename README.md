# Technical design for a URL Shorten
## Functional Requirement:
* User should input a long URL and service should generate a shorter URL. _We are not considering custom short links by users in this solution._
* When user hits the shorter link our service should redirect to the original longer URL.

## Non Functional Requirement:
* It should be highly scalable, with low latency & high availability.
* The short links shouldn't be predictable.

# Option: 1 - Scalable Architecture Design: Assumptions & Solution:
### Assumptions:
* We are creating a short URL with 8 Char length.
* We have a short domain name registered.
* **Traffic**
  1. Lets assume we request for 1 new short URL and the Short URL is used 100 times for redirection , so the ratio between write and read would be 1:100 --> System is read heavy.
  2. So lets say we have 200 short URL create requests per second a month: So for a month we have : _30 days * 24 hours *3600 Sec *200 = ~500M requests_
  3. So with ~500M short URL request we will have _500M*100 = 50 Billion redirection request_
* **Storage**
  1. So lets assume the system stores all the URL shortening request and their shortened link for 5 years. As we expect to have 500M new URLs every month, the total number of objects we expect to store will be _500 M * (5 * 12) months = 30 B._
  2. Now let’s assume that each stored object will be approximately 100 bytes. We will need total storage of _30 billion * 100 bytes = 3 TB._
* **Cache**
  1. We want to cache some of the popular URLs that are frequently accessed and if we follow the 80–20 rule, meaning we keep a 20% request from the cache.
  2. Since we have 20K redirection requests/second, we will be getting _20K * 60 seconds* 60 minutes * 24 hours = ~1.7 billion per day. If we plan to cache 20% of these requests, we will need _0.2 * 1.7 billion * 100 bytes = ~34GB of memory._ 

### Database: So we can use a NOSQL DB like DynamoDB which would be easier to scale as each URL data is independent of each other and we can store billions of records.
### The Short URL: 
* Unique key can be generated either by [62bit encoder- Python Code](https://github.com/AmitVerma-Learn/URLShortner/blob/457b3f751f8471aade03eedede29c9fcf490e28d/Encoder62.py) and can be used along with distributed service of Apache Zookeeper for managing counters for multiple app servers for Scalability and using the same encoding mechanism to generate Short URL.
* Or by using a scalable Unique Key Generation Service (multiple server) which can store data in a Key-DB with a backup all to maintain availability and removing single point of failure.
![Scalable Architecture Design](https://github.com/AmitVerma-Learn/URLShortner/blob/510da7c0f6197e1bf2530ac6e28fe29d678e2861/URLShortner.drawio.png)

# Option: 2 - AWS Serverless Architecture Design: Assumptions & Solution:
### Assumptions:
* We are creating a short URL with 8 Char length.
* We have to register a short domain name.
* We will use 100% AWS serverless architecture.
### We develop a Lambda function that does the URL shortening magic and integrate it with the following 6 Amazon Webservices:  
* Amazon API Gateway: _To setup a REST API endpoint which internet browser could reach and through which URL shortener and its features can be accessed_
* Amazon CloudFront: _To configure static content caching and HTTP to HTTPS redirection as REST API endpoints can be reached only using https protocol_
* Amazon DynamoDB: _To have persistent storage to hold the URL pairs (long URL, short URL)_
* Amazon Route 53: _To register a short domain name for your URL shortener service_
* AWS Certificate Manager: _To generate SSL certificates for your CloudFront distribution_
* AWS Identity and Access Management: _To be able to attach DynamoDB access policy to your Lambda function so that Lambda can do "reads/writes" to your DynamoDB table_ 

### This Lambda function handles these 3 types of requests:

* Requests to render 'URL shortener' web page, i.e. fetch static web content from the Lambda storage and output it (green lines in the architecture scheme)
* Requests to shorten long URLs, i.e. use algorithm (8 Character Random Generator) to convert long URL into short one, store in DB and include in the web page content (yellow lines in the architecture scheme)
* Requests to redirect users accessing short URL to the original longer URL (orange lines in the architecture scheme).
  1. In case there is a match between the short URL user requested to visit and the short URL located in the Amazon DynamoDB table, Lambda function issues HTTP status code 301 (Moved permanently) and by using the Location field in the HTTP response header redirects user to the target (long) URL,
  2. In case there is no match, HTTP status code 404 (Not Found) is issued.  

### 8 Character Random Generator: 
* Algorithm that generates the path part of the short URL is the following: [RandomGenerator - JavaScript](https://github.com/AmitVerma-Learn/URLShortner/blob/510da7c0f6197e1bf2530ac6e28fe29d678e2861/generator.js).
* We take the current number of "milliseconds that elapsed since 1st January 1970 till this moment of Lambda function execution" and convert it into a radix-36 representation. This results in having only 8 characters.
* If exactly the same long URL was shortened in the past, we won't generate a brand new short URL representation of it, but rather provide the user with the already existing short URL by checking in the DynamoDB.

![Serverless Architecture Scheme](https://github.com/AmitVerma-Learn/URLShortner/blob/046f838a02b345c6773bbdd3192a6cfd054220fe/Serverlesss%20Architecture%20Scheme.drawio.png)
