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

global class {{ api_name }} implements Database.Batchable<sObject> {
	
	String query;
	
	global {{ api_name }}() {
		
	}
	
	global Database.QueryLocator start(Database.BatchableContext BC) {
		return Database.getQueryLocator(query);
	}

   	global void execute(Database.BatchableContext BC, List<sObject> scope) {
	
	}
	
	global void finish(Database.BatchableContext BC) {
		
	}
}