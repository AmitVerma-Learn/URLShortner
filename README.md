# Technical design for a URL Shorten
## Functional Requirement:
* User should input a long URL and service should generate a shorter URL. _We are not considering custom short links by users in this solution._
* When user hits the shorter link our service should redirect to the original longer URL.

## Non Functional Requirement:
* It should be highly scalable, with low latency & high availability.
* The short links shouldn't be predictable.

# Assumptions:
* We are creating a short URL with 8 Char length.
* We have a short domain name registered.
* **Traffic**
  1. Lets assume we request for 1 new short URL and the Short URL is used 100 times for redirection , so the ratio between write and read would be 1:100 --> System is read heavy.
  2. So lets say we have 200 short URL create requests per second a month: So for a month we have : _30 days * 24 hours *3600 Sec *200 = ~500M requests_
  3. So with ~500M short URL request we will have _500M*100 = 50 Billion redirection request_
* **Storage**
  1. 



# Option: 1 - Scalable Architecture Design

![Scalable Architecture Design](https://github.com/AmitVerma-Learn/URLShortner/blob/3c20fefcc9a3f54328e75cb32a018150b03ce43d/URLShortner.drawio.png)
### [62bit encoder- Python Code](https://github.com/AmitVerma-Learn/URLShortner/blob/457b3f751f8471aade03eedede29c9fcf490e28d/Encoder62.py)
