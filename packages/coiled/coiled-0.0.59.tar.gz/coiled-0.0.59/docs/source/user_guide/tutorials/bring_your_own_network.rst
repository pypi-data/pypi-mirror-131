======================
Bring your own network
======================

.. note::
  This feature is currently experimental, with new features under active
  development.

Usually Coiled creates all the cloud networking resources required for running a cluster. For customers who are hosting Coiled in their own AWS or GCP account, we also provide the option to have Coiled use an existing network which you have created.

While this means you're responsible managing more aspects of hosting Coiled, it also enables you to run Coiled while meeting specific needs for network security or configuration, such as:

- you need to peer the VPC used for Coiled clusters with other networks
- you need to configure additional network security, for example, routing traffic through a customer-managed firewall or limiting inbound connections to a VPN
- you need to configure network access to your data sources, for example, adding private links
- you need to limit the AIM permissions that you grant to Coiled

If you provide a network for Coiled to use, you'll be responsible for:

- VPC
- subnet(s)
- routing and internet access (including NAT for VMs without public IP address)
- security group (AWS) or firewall rules (GCP)

If you provide a network, Coiled will still be responsible for creating VMs (and associated storage, network interface, and public IP if appropriate) as well as machine images and Docker images (for your software environments).


Network requirements
--------------------

See :ref:`network-architecture` for details about the networking needs of a Coiled cluster.

For an example of one way to configure a cluster network, here's what we do when we create networks in AWS:

There's a **VPC** with an **Internet Gateway** and two **subnets**.

One subnet is a *public* subnet assigned for cluster scheduler VMs. This subnet contains **NAT Gateway** (used for workers to access internet), and route table with local route for VPC and default route (``0.0.0.0/0``) to **Internet Gateway**.

When we create scheduler, we assign it public IP; this enables it to download required software without using NAT Gateway, and also (in the default configuration) is used so your local client can connect to the scheduler.

The other subnet is a *private* subnet assigned for cluster worker VMs. Since the worker VMs need to be able to download software as well as communicate with the scheduler, this subnet has route table with local route for VPC and default route (``0.0.0.0/0``) to the **NAT Gateway** in the public subnet.

The security group used for the cluster allows ingress on ports 8787 and 8786 from anywhere (``0.0.0.0/0``), ingress on any port from inside the security group (for communication between VMs in the cluster), and egress on any port to anywhere.

The network you provide for Coiled to use needn't exactly match the networks we create by default, but they do need to meet some minimal requirements.

Our default network allows internet access to the scheduler. This isn't a requirement, so long as the machine running the Python client is able to connect to the scheduler. For instance, you could be running the client on a machine inside a paired VPC or go through a VPC which allows you to connect to private IP of the scheduler. Ports 8786, 8787 need to be open for ingress so that the client can connect to scheduler.

Our default network uses an Internet Gateway and NAT Gateway. It's necessary that the scheduler and workers be able to download software (as well of course as any data used in your computations). It's not necessary that this access be through an Internet Gateway and NAT Gateway in the same VPC. For instance, you could have a default route that goes a firewall you with to use for egress to the internet.


Configuring Coiled to use your network
--------------------------------------

At present the only way to configure Coiled to use your network is to use the Python API to set your account backend options.

For AWS, this would look like so:

.. code-block::

  import coiled

  coiled.set_backend_options(
    backend="aws",
    customer_hosted=True,
    aws_access_key_id="...",
    aws_secret_access_key="...",
    network={
      "network_id":"vpc-12345678",
      "scheduler_subnet_id":"subnet-12345678",
      "worker_subnet_id":"subnet-87654321",
      "firewall_id":"sg-12345678"  # security group
    }
  )

The resource IDs are not the full ARN, just the ID.

For GCP, you can provide credentials as a file with your key-pair, like so:

.. code-block::

  coiled.set_backend_options(
    backend_type="gcp",
    gcp_service_creds_file="/path/to/my-gcp-key.json",
    gcp_project_id="my-project-id",
    gcp_region="us-east1",
    gcp_zone="us-east1-c",
    registry_type="gar",
    customer_hosted=True,
    network={
      "network_id":"https://www.googleapis.com/compute/v1/projects/my-project-id/global/networks/byo-network",
      "scheduler_subnet_id":"https://www.googleapis.com/compute/v1/projects/my-project-id/regions/us-east1/subnetworks/byo-subnet",
      "worker_subnet_id":"https://www.googleapis.com/compute/v1/projects/my-project-id/regions/us-east1/subnetworks/byo-subnet",
      "firewall_id":"byo-firewall"  # network tag
    }
  )

