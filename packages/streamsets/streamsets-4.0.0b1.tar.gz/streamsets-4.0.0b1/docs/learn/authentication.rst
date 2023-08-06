Authentication
==============
|

StreamSets DataOps Platform SDK for Python uses API Credentials for authentication.

For more details, refer to the `StreamSets DataOps Platform Documentation <https://docs.streamsets.com/portal/#platform-controlhub/controlhub/UserGuide/OrganizationSecurity/APICredentials_title.html#concept_vpm_p32_qqb>`_.

Create API Credentials
~~~~~~~~~~~~~~~~~~~~~~
Using a web browser log into StreamSets DataOps Platform.

In the UI, API Credentials are as seen below:

.. image:: ../_static/images/learn/api_credentials.png
|

Create new API credentials by referring to the `StreamSets DataOps Platform Documentation <https://docs.streamsets.com/portal/#platform-controlhub/controlhub/UserGuide/OrganizationSecurity/APICredentials_title.html#task_jsq_h3f_qqb>`_.

For the purpose of this documentation, the above API Credentials will be referred as <credential ID> and <token>.


Connecting to Control Hub
~~~~~~~~~~~~~~~~~~~~~~~~~

Connect to Control Hub by creating an instance of :py:class:`streamsets.sdk.ControlHub`, passing in
the URL of your Control Hub instance (as shown in your browser once logged in) and API Credentials.

Using the example URL of https://na01.hub.streamsets.com:

.. code-block:: python

    # Connect to the StreamSets DataOps Platform.
    sch = ControlHub('https://na01.hub.streamsets.com', credential_id=<credential ID>, token=<token>)
