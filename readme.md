# ALTR

This is a simple webapp to allow the selection and downloading of alternative files from ResourceSpace. The immediate use case is for staff who need to access cropped versions (at standardized pixel dimensions) of an original image for use in our program guide or website.

# Dependencies

`pip3 install bottle requests`

This uses the [Bottle](https://bottlepy.org/docs/dev/index.html) webapp framework, which itself only uses the Python standard library. The app also uses the `requests` module. Bootstrap styling is included using CDN links.

## Usage


* Make your cropped selections in ResourceSpace, make sure that they are marked with the correct type (e.g. "web crop")
* Put all the resources with crops you want into a collection in ResourceSpace
* From the collection "Actions" menu choose "Download metadata CSV"
* Open the csv and copy the resource IDs from the first column, then paste them into a plain text file
* There should be one ID per line, nothing else (no other text, etc.)
* Upload the text file to altr and select the correct type ("web crop" or whatever)
* Your files will get wrapped in a zip archive that you can then download
