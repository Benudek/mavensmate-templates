<project name="Sample usage of Salesforce Ant tasks" default="test" basedir="." xmlns:sf="antlib:com.salesforce">

    <property file="build.properties"/>
    <property environment="env"/>

    <!-- Setting default value for username, password and session id properties to empty string
         so unset values are treated as empty. Without this, ant expressions such as ${sf.username}
         will be treated literally.
    -->
    <condition property="sf.username" value=""> <not> <isset property="sf.username"/> </not> </condition>
    <condition property="sf.password" value=""> <not> <isset property="sf.password"/> </not> </condition>
    <condition property="sf.sessionId" value=""> <not> <isset property="sf.sessionId"/> </not> </condition>

    <taskdef resource="com/salesforce/antlib.xml" uri="antlib:com.salesforce">
        <classpath>
            <pathelement location="../ant-salesforce.jar" />         	
        </classpath>
    </taskdef>

    <!-- Test out deploy and retrieve verbs for package 'mypkg' -->
    <target name="test">
      <!-- Upload the contents of the "mypkg" package -->
      <sf:deploy username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" deployRoot="mypkg" rollbackOnError="true"/>
      <mkdir dir="retrieveOutput"/>
      <!-- Retrieve the contents into another directory -->
      <sf:retrieve username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" retrieveTarget="retrieveOutput" packageNames="MyPkg"/>
    </target>

    <!-- Retrieve an unpackaged set of metadata from your org -->
    <!-- The file unpackaged/package.xml lists what is to be retrieved -->
    <target name="retrieveUnpackaged">
      <mkdir dir="retrieveUnpackaged"/>
      <!-- Retrieve the contents into another directory -->
      <sf:retrieve username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" retrieveTarget="retrieveUnpackaged" unpackaged="unpackaged/package.xml"/>
    </target>

    <!-- Retrieve all the items of a particular metadata type -->
    <target name="bulkRetrieve">
      <sf:bulkRetrieve username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" metadataType="${sf.metadataType}" retrieveTarget="retrieveUnpackaged"/>
    </target>

    <!-- Retrieve metadata for all the packages specified under packageNames -->
    <target name="retrievePkg">
      <sf:retrieve username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" retrieveTarget="retrieveOutput" packageNames="${sf.pkgName}"/>
    </target>

    <!-- Deploy the unpackaged set of metadata retrieved with retrieveUnpackaged and run tests in this organization's namespace only-->
    <target name="deployUnpackaged">
      <sf:deploy username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" deployRoot="retrieveUnpackaged" rollbackOnError="true"/>
    </target>

    <!-- Deploy a zip of metadata files to the org -->
    <target name="deployZip">
      <sf:deploy username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" zipFile="${sf.zipFile}" pollWaitMillis="1000" rollbackOnError="true"/>
    </target>

    <!-- Shows deploying code & running tests for code in directory -->
    <target name="deployCode">
      <!-- Upload the contents of the "codepkg" directory, running the tests for just 1 class -->
      <sf:deploy username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" deployRoot="codepkg" testLevel="RunSpecifiedTests" rollbackOnError="true">
				<runTest>FSM_ServiceAppointmentSchedulerTests</runTest>
				<runTest>ServiceAppointmentRSOTests</runTest>
				<runTest>FSM_SA_TriggerHandler_RSORejectTest</runTest>
				<runTest>FSM_DMLBufferTests</runTest>
				<runTest>FSM_WorkOrderHelperTests</runTest>
				<runTest>OperatingHoursTriggerHandlerTests</runTest>
				<runTest>ServiceAppointmentTriggerTests</runTest>
				<runTest>FSM_ServiceTerritoryTriggerTest</runTest>
				<runTest>WorkOrderTriggerTests</runTest>
				<runTest>ProductRequestTriggerHandlerTests</runTest>
				<runTest>FSM_WorkOrderSLACalculatorTests</runTest>
				<runTest>FSM_SiteVisitHandlerTests</runTest>
				<runTest>FSM_WorkOrderHelperTestMore</runTest>
				<runTest>FSM_AllowedWorkOrderTests</runTest>
				<runTest>Product2TriggerHandlerTests</runTest>
				<runTest>FSM_OperatingHoursHelperTests</runTest>
				<runTest>FSM_SAWorkHourFlagTest</runTest>
				<runTest>LocationTriggerTests</runTest>
				<runTest>FSM_WorkOrderSLACalculatorOver8DaysTest</runTest>
				<runTest>FSM_ServiceContractSharingTest</runTest>
				<runTest>FSM_PayCalendarSearchTests</runTest>
				<runTest>FSM_ContactTriggerActionsTests</runTest>
				<runTest>ProductConsumedTriggerHandlerTests</runTest>
				<runTest>ServiceAppointmentTriggerHandlerTests</runTest>
				<runTest>FSM_RSOHelperTests</runTest>
				<runTest>FSM_WorkOrderAssetHelperTests</runTest>
				<runTest>FSM_ServiceTerritoryTriggerTests</runTest>
				<runTest>FSM_GlobalsTests</runTest>
				<runTest>FSM_CaseTriggerActionsTests</runTest>
				<runTest>WorkOrderTriggerHandlerTests</runTest>
				<runTest>FSM_ServiceContractSharingBatchJobTests</runTest>
				<runTest>Location_ContactTriggerTests</runTest>
				<runTest>FSM_SetAssetActCalloutEntBatchJobTests</runTest>
				<runTest>FSM_ServiceResourceOptimizeCtrlTest</runTest>
				<runTest>FSM_ServiceNeedHelperTests</runTest>
				<runTest>FSM_NotificationsHelperTests</runTest>
				<runTest>FSM_ServiceTerritoryHelperTests</runTest>
      </sf:deploy>
   
    </target>

	 <!-- Shows deploying code with no TestLevel sepcified -->
    <target name="deployCodeNoTestLevelSpecified">
      <sf:deploy username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" deployRoot="codepkg" rollbackOnError="true"/>
    </target>

	<!-- Shows deploying code and running tests only within the org namespace -->
	<target name="deployCodeRunLocalTests">
	  <sf:deploy username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" deployRoot="codepkg" rollbackOnError="true"  testlevel="RunLocalTests"/>
	</target>

    <!-- Shows removing code; only succeeds if done after deployCode -->
    <target name="undeployCode">
      <sf:deploy username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" deployRoot="removecodepkg"/>
    </target>

    <!-- Shows retrieving code; only succeeds if done after deployCode -->
    <target name="retrieveCode">
      <!-- Retrieve the contents listed in the file codepkg/package.xml into the codepkg directory -->
      <sf:retrieve username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" retrieveTarget="codepkg" unpackaged="codepkg/package.xml"/>
    </target>

    <!-- Shows deploying code, running all tests, and running tests (1 of which fails), and logging. -->
    <target name="deployCodeFailingTest">
      <!-- Upload the contents of the "codepkg" package, running all tests -->
      <sf:deploy username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" deployRoot="codepkg" testLevel="RunAllTestsInOrg" rollbackOnError="true" logType="Debugonly"/>
    </target>

    <!-- Shows check only; never actually saves to the server -->
    <target name="deployCodeCheckOnly">
      <sf:deploy username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" deployRoot="codepkg" testLevel="RunSpecifiedTests" checkOnly="true"/>
				<runTest>FSM_ServiceAppointmentSchedulerTests</runTest>
				<runTest>ServiceAppointmentRSOTests</runTest>
				<runTest>FSM_SA_TriggerHandler_RSORejectTest</runTest>
				<runTest>FSM_DMLBufferTests</runTest>
				<runTest>FSM_WorkOrderHelperTests</runTest>
				<runTest>OperatingHoursTriggerHandlerTests</runTest>
				<runTest>ServiceAppointmentTriggerTests</runTest>
				<runTest>FSM_ServiceTerritoryTriggerTest</runTest>
				<runTest>WorkOrderTriggerTests</runTest>
				<runTest>ProductRequestTriggerHandlerTests</runTest>
				<runTest>FSM_WorkOrderSLACalculatorTests</runTest>
				<runTest>FSM_SiteVisitHandlerTests</runTest>
				<runTest>FSM_WorkOrderHelperTestMore</runTest>
				<runTest>FSM_AllowedWorkOrderTests</runTest>
				<runTest>Product2TriggerHandlerTests</runTest>
				<runTest>FSM_OperatingHoursHelperTests</runTest>
				<runTest>FSM_SAWorkHourFlagTest</runTest>
				<runTest>LocationTriggerTests</runTest>
				<runTest>FSM_WorkOrderSLACalculatorOver8DaysTest</runTest>
				<runTest>FSM_ServiceContractSharingTest</runTest>
				<runTest>FSM_PayCalendarSearchTests</runTest>
				<runTest>FSM_ContactTriggerActionsTests</runTest>
				<runTest>ProductConsumedTriggerHandlerTests</runTest>
				<runTest>ServiceAppointmentTriggerHandlerTests</runTest>
				<runTest>FSM_RSOHelperTests</runTest>
				<runTest>FSM_WorkOrderAssetHelperTests</runTest>
				<runTest>FSM_ServiceTerritoryTriggerTests</runTest>
				<runTest>FSM_GlobalsTests</runTest>
				<runTest>FSM_CaseTriggerActionsTests</runTest>
				<runTest>WorkOrderTriggerHandlerTests</runTest>
				<runTest>FSM_ServiceContractSharingBatchJobTests</runTest>
				<runTest>Location_ContactTriggerTests</runTest>
				<runTest>FSM_SetAssetActCalloutEntBatchJobTests</runTest>
				<runTest>FSM_ServiceResourceOptimizeCtrlTest</runTest>
				<runTest>FSM_ServiceNeedHelperTests</runTest>
				<runTest>FSM_NotificationsHelperTests</runTest>
				<runTest>FSM_ServiceTerritoryHelperTests</runTest>
    </target>

	<!-- Shows quick deployment of recent validation. Set the property sf.recentValidationId to your recent check only deployment Id -->
	<target name="quickDeploy">
	  <sf:deployRecentValidation  username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" recentValidationId="${sf.recentValidationId}"/>
	</target>

	<!-- Shows cancel deployment of deploy request either pending or in progress. Set property sf.requestId to Id of pending or in progress deploy request -->
	<target name="cancelDeploy">
	  <sf:cancelDeploy  username="${sf.username}" password="${sf.password}" serverurl="${sf.serverurl}" maxPoll="${sf.maxPoll}" requestId="${sf.requestId}"/>
	</target>

	<!-- Retrieve the information of all items of a particular metadata type -->
    <target name="listMetadata">
      <sf:listMetadata username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}" metadataType="${sf.metadataType}"/>
    </target>

	<!-- Retrieve the information on all supported metadata type -->
    <target name="describeMetadata">
      <sf:describeMetadata username="${sf.username}" password="${sf.password}" sessionId="${sf.sessionId}" serverurl="${sf.serverurl}"/>
    </target>
</project>
