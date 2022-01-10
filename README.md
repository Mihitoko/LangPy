#Langpy
###A library to localizing apps


Langpy is build for quickly setting up multi-language applications by building a python package for you. <br>
For that Langpy utilizes .yaml files to read out your desired language structure and parse it into python code.

###Features
 - Auto generating templates. You just need to put in the translation.
 - String formatting with parameter hints.
 - Parameter validation

###Parameter validation
<p>
Langpy support passing format strings as values.
When the library parses the yaml file it will autodetect format strings and check if the string uses the same
parameters for all languages. This helps to reduce runtime errors.
</p>

##Commands
The three main commands are:

>langpy init

This sets up a langpy project and generates a config template for you.

>langpy new "language"

Creates a new language template based on your default template.<br>
Replace "language" with you desired language **de** for example

>langpy compile

After everything is set up this will parse your yaml files into python code and will check for 
parameter signature.
<br><br>
For more information look in the **docs** folder.