/**********************************************************************
 Name: {{api_name}}
 Other classes used:
 Tested in class:
======================================================
Description: 
	Sample description
======================================================
History                                                            
-------                                                            
VERSION         AUTHOR                  DATE            DETAIL                                 
1.0             John Doe  				29/08/1997		Initial development
***********************************************************************/

public with sharing class {{ api_name }} {

	private final sObject mysObject;

    // The extension constructor initializes the private member
    // variable mysObject by using the getRecord method from the standard
    // controller.
    public {{ api_name }}(ApexPages.StandardController stdController) {
        this.mysObject = (sObject)stdController.getRecord();
    }
}