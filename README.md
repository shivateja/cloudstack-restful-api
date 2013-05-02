#CloudStack RESTful API
A RESTful, flask wrapper API on CloudStack API.

*Warning: Not RESTful at present state. Just a prototype.*

###Mappings
 * GET /subject/verb?params -> GET verbSubject?params
 * GET /subject -> either listSubject or getSubject
 * POST /subject -> GET createSubject?params
 * PUT /subject -> GET updateSubject?params
 * DELETE /subject -> GET deleteSubject?params
 
##What's wrong?
Only few actions like list, get, create, delete etc have been mapped with proper HTTP methods.
The rest still remain as query based with just camel case removed.
