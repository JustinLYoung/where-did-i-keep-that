I looked into using Python's qrcode library for generating QR codes for our storage locations. The library works with Pillow to create QR codes as PNG images, which we could allow users to download and print as labels. We already have both packages included in our requirements.txt, so we wouldn't need to add anything else.

The idea is that when a user creates a storage location, it will have a unique ID in the database. We can use that ID to generate a URL for the location and turn that URL into a QR code. When someone scans the code with their phone, it would open the corresponding page and show the items stored there.

I also created a small Python prototype to test generating QR codes using a sample URL. This is just a prototype for now, but we can use it when we start building the actual feature.

One advantage of this library is that it's relatively simple to use and doesn't require an external API. One thing we'll need to consider is that QR codes should point to an accessible URL rather than localhost, especially if users are scanning them from their phones. We'll also need to make sure users can only view storage locations they're authorized to access.

We'll also need to make sure the QR codes work with how we're storing locations in the database and decide on the final URL structure for each location.

Reference: https://pypi.org/project/qrcode/