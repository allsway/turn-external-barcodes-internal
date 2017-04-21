# Switches an external ID field to an internal field
Changes a selected user ID field from an external field to an internal field (so that user records can be overlaid by the SIS load but have a unique identifier not included in the load retained)

# config.txt
[Params]
apikey: [apikey] 
baseurl: https://api-na.hosted.exlibrisgroup.com
idtype: [BARCODE]
total: [total users]

# switch_to_internal.py
Goes through each user record from {offset} to {total users} and checks for a user_identifier equal to 'idtype'.  Updates the attribute 'segment_type' to 'Internal' for all ids that match idtype.  

Run as 
`python ./switch_to_internal.py config.txt {offset}`

