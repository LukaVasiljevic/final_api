# NST & YOLO API

API combining YOLO Object Segmentation and Neural Style Transfer 

## Description

This API allows you to perform object segmentation using YOLOv8 and apply neural style transfer to images in 3 different modes. The main goal is to segment selected classes and apply style to the class/ these classes or whole image. Execution time is 0.5s - 1.3s per call and it can vary depending on the server.  

## Endpoints

### Get YOLO Model classes

**Endpoint:** `/get-classes`

**Method:** GET

**Description:** Retrieves the list of YOLO model classes available for object segmentation

**Response:**
```json
{
   {
    "0": "person",
    "1": "bicycle",
    "2": "car",
    "3": "motorcycle",
    "4": "airplane",
    ...
    }
}
```
### Get Neural Style Transfer trained models

**Endpoint:** `/get-styles`

**Method:** GET

**Description:** Retrieves the list of style models that can be applied for Neural Style Transfer.

**Response:**
```json
{
    [
    {
        "author": "Eugène Delacroix",
        "description": "",
        "model_id": "",
        "title": "Liberty Leading the People",
        "year": 1830
    },
    {
        "author": "Salvador Dali",
        "description": "",
        "model_id": "",
        "title": "The Persistence of Memory",
        "year": 1931
    },
    {
        "author": "Petar Lubarda",
        "description": "",
        "model_id": "",
        "title": "Crni Panter",
        "year": 1968
    },
    {
        "author": "Petar Lubarda",
        "description": "",
        "model_id": "",
        "title": "Konji",
        "year": 1953
    },
    {
        "author": "Uros Predic",
        "description": "",
        "model_id": "",
        "title": "Vesela Braca",
        "year": 1887
    },
    {
        "author": "Dragos Kalajic",
        "description": "",
        "model_id": "",
        "title": "Sokolarka",
        "year": 2001
    },
    ...
]
}
```

### Process Image

**Endpoint:** `/process-image`

**Method:** POST

**Description:** Applies object segmentation and neural style transfer to the provided image.

**Request:**

You can use example request listed in the repository by name `send_request.py`.

- `image`: The image file to be processed.
- `info`: Additional information containing the following fields:
  - `style`: The `model_id` value of selected style to be applied for Neural Style Transfer
  - `mode`: The mode for applying the style. Possible values: "CLASS_MODE", "INVERSE_MODE", "FULL_STYLE_MODE".

**Response:**
```
{
  "execution_time": "1.42",
  "processed_image_path": "http://localhost:5000/static/processed_images/b1daf3ac-3585-4aaa-a292-27bd7cc33926.jpg"
}
```
The API will respond with the link to modified image based on the applied object segmentation and neural style transfer.

## How to run API 

to be done.. 


## Usage

To use the API, make requests to the provided endpoints using the appropriate HTTP methods.

Example usage with cURL:
to be done.. 

## Attribution
add the attribution 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact

For any questions or inquiries, please contact lukav217@gmail.com
