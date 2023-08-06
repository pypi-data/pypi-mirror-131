# JsonNode Implementation

This drb-impl-json module implements json format access with DRB data model. It is able to navigates among the json
contents.

## Json Factory and Json Node

The module implements the basic factory model defined in DRB in its node resolver. Based on the python entry point
mechanism, this module can be dynamically imported into applications.

The entry point group reference is `drb.impl`.<br/>
The implementation name is `json`.<br/>
The factory class is encoded into `drb_impl_json.json_node_factory`.<br/>

The json factory creates a JsonNode from an existing json content. It uses a base node to access the content data using
the streamed base node implementation.

The base node can be a FileNode (See drb-impl-file), HttpNode, ZipNode or any other node able to provide
streamed (`BufferedIOBase`, `RawIOBase`, `IO`) json content.

## limitations

The current version does not manage child modification and insertion. JsonNode is currently read only.

## Using this module

To include this module into your project, the `drb-impl-json` module shall be referenced into `requirement.txt` file, or
the following pip line can be run:

```commandline
pip install drb-impl-json
```

### Node Creation:

The implementation can create a JsonNode by giving the path to a json file:

```
from drb_impl_json import DrbJsonNode

node = JsonNode(PATH_JSON)
```

the implementation can also give a dictionary in argument:

```
from drb_impl_json import DrbJsonNode

DICT = { 
        "id":"01", 
        "name": "Tom", 
        "lastname": "Price" 
     }
node = JsonNode(NAME_OF_YOUR_NODE, data = DICT)
```

If the baseNode is an HttpNode, FileNode... the implementation can retrieve the data of your Json with this:

 ```
from drb_impl_json import JsonNodeFactory

FACTORY = JsonNodeFactory()
FILE_NODE = DrbFileNode(PATH_TO_YOUR_JSON)
NODE = FACTORY.create(FILE_NODE)
```

### Different types of data

| data | JSON Type | Python Type |
| :---- | :--------- | :----------- |
| null | null | None |
| true/false | boolean | bool |
| 'hello World' | string | str |
|  1 | int | int |
|  1.0 | number | float |
|  [...] | array | list |
|  {...} | object | dict |