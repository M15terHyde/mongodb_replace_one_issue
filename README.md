# mongodb_replace_one_issue
The files needed from my project which reproduce the false positive filter issue in replace_one with upsert=True

1) Download the repo
2) cd into ./database/mongo ; docker-compose up --build -d
3) you may want to open a new terminal because the next step will soak up the existing terminal
4) cd into ./products ; docker-compose up --build
5) python test.py

# Background:
I'm creating a mock-up store inventory database.
It is meant to manage store locations and products in these store from many different businesses.
To avoid locationID and productID collisions between these different businesses a foreignAPIauthority string is used to identify each businesses to seperate their namespaces.

This way:

{foreignAPIauthority:'business1', locationID:'1'}

is a different location from

{foreignAPIauthority:'business2', locationID:'1'}

Each business chain can have many locationIDs and many productIDs
In the same way locationID can be reused in different namespaces and be unique I need productIDs to be able to be reused in different locations within the same business.

So:
{foreignAPIauthority:'business1', locationID:'1', productID:'1'}

is a different physical entity from:

{foreignAPIauthority:'business1', locationID:'2', productID:'1'}

TLDR: It requires all three of these values to uniquely identify any product. Therefore that's the filter I use when calling replace_one


# What happens:
This test is meant to do 2 things:

1) It's meant to upload 10 products. 8 of which are meant to be used in further tests I have not included in this repo because they are not important to reproduce the false positive bug I'm seeing.

2) This test included (test1) is also meant to test the /addone endpoint in products.py whose functionality is to add (upsert) the product if it does not already exist or update (replace) the existing if it does already exist. Products 1 & 2 are to be inserted. Then product 3 is meant to duplicate 1 and 4 is meant to duplicate 2 to test non-duplication.


# Results:
product 3 correctly updates (replaces) product 1
oddly enough product 4 incorrectly udpdates (replaces) product 3, even though they have different productIDs.
replace_one's filter is returning a false positive match saying product3 matches the filter when in fact it does not.

Here's the test script result I got as an example:
```
    product1 inserted objectID: 61ec70e2e0ea2044bc4bd7cf
    product2 inserted objectID: 61ec70e3e0ea2044bc4bd7d1
    product3 inserted objectID: 61ec70e2e0ea2044bc4bd7cf  (Correctly updates product1)
    product4 inserted objectID: 61ec70e2e0ea2044bc4bd7cf  (Incorrectly updates product3 (aka product1) instead of product2)
    product5 inserted objectID: 61ec70e3e0ea2044bc4bd7d7
    product6 inserted objectID: 61ec70e3e0ea2044bc4bd7d9
    product7 inserted objectID: 61ec70e3e0ea2044bc4bd7db
    product8 inserted objectID: 61ec70e3e0ea2044bc4bd7dd
    product9 inserted objectID: 61ec70e3e0ea2044bc4bd7df
    product10 inserted objectID: 61ec70e4e0ea2044bc4bd7e1
TEST1: Insert Feature: PASS
TEST1: Non-duplication: FAIL
```

For demonstration purposes. Feel free to download and share as you see fit.
