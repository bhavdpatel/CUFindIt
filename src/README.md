# CUFindIt
/api/items/  method = Get
^ get all items

Response Body:
{
	“items” : [
	 {
	“items” : [
	  {
		“id” : 1,
		“name” : “headphones”,
		“image_name” : “_____”,
		“location” : “Upson Hall”,
            "date_found": “12/20/2021”,
           		"date_claimed": “ ”,
            	"id_found": “li200”,
           		"id_claimed" : “ ”
        },
        {
		“id” : 2,
		“name” : “backpack”,
		“image_name” : “_____”,
		“location” : “Duffield Hall”,
            "date_found": “12/22/2021”,
           		"date_claimed": “ ”,
            	"id_found": “isp22”,
           		"id_claimed" : “ ”
        },
..
	]
}







/api/items/  method = post
^ addes a lost item to database

Request Body:
{
	“name” : <USER INPUT>,
	“image” : <USER INPUT>,
	“location” : <USER INPUT>,
	“date_found” : <USER INPUT>,
	“id_found” : <USER INPUT>
}

Response Body:

{
	“id” : <AUTO INCREMENTED>,
	“name” : <USER INPUT>,
	“image_name” : <USER INPUT>,
	“location” : <USER INPUT>,
"date_found": <USER INPUT>,
     "date_claimed": “”,
     "id_found": <USER INPUT>,
     "id_claimed" : “”
}




/api/items/<id>/ method = get
^ get item info 

Response Body:
{
	“id” : <AUTO INCREMENTED>,
	“name” : <USER INPUT>,
	“image_name” : <USER INPUT>,
	“location” : <USER INPUT>,
"date_found": <USER INPUT>,
     "date_claimed": “”,
     "id_found": <USER INPUT>,
     "id_claimed" : “”
}



/api/items/<id>/ method = update
^ update item, if claimed, with netid of user

Response Body:
{
	“id” : <AUTO INCREMENTED>,
	“name” : <USER INPUT>,
	“image_name” : <USER INPUT>,
	“location” : <USER INPUT>,
"date_found": <USER INPUT>,
     "date_claimed": <USER INPUT>,
     "id_found": <USER INPUT>,
     "id_claimed" : <USER INPUT>
}




/api/items/<id>/ method = delete 
^ delete an item from database

Response Body:
{
	“id” : <AUTO INCREMENTED>,
	“name” : <USER INPUT>,
	“image_name” : <USER INPUT>,
	“location” : <USER INPUT>,
"date_found": <USER INPUT>,
     "date_claimed": “”,
     "id_found": <USER INPUT>,
     "id_claimed" : “”
}





