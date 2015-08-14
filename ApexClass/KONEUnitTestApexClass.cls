/**********************************************************************
 Name: {{api_name}}
 Other classes used:
======================================================
Description: 
	Sample description
======================================================
History                                                            
-------                                                            
VERSION         AUTHOR                  DATE            DETAIL                                 
1.0             John Doe  				29/08/1997		Initial development
***********************************************************************/

/* NOTE on Test Factories
 * There is a number of utility classes (Test Factories) which provide
 * helper methods for test data creation such as custom settings, users
 * user roles, standard accounts contacts and opportunities.
 * Use: 
 * TestFactory for general functionality
 * TestFactoryScorecard for Sales Cockpit unit tests
 * cpTestFactory for KONE Care Online unit tests
 */
 
@isTest
private class {{ api_name }} {
	
	@testSetup
    static void createTestData() {
		// Set up test data for test methods
	}
	
	static testMethod void test_method_one() {
		// Implement test code
	}	
}