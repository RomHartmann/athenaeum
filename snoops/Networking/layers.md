# Networking layers - OSI model

OSI = Open System Interconection.
Model that defiens a networking framework to implement protocols in 7 layers.


## Layer 7 - Application
- End user processes
- Communication partners identified, authentication, privacy, quality of service.
- Eg www browers, NFS, HTTP, FTP etc.

## Layer 6 - Presentation
(Sometimes called syntax layer)
- Translates application to network format (and vice versa)
- Formats and encrypts data to be sent across a network.

## Layer 5 - Session
- Establishes, manages and terminates connections between applications.

## Layer 4 - Transport
- Transparent transfer of data between end systems (hosts)
- Responsible for end-to-end error recovery and flow control
- ensures complete data transfer

## Layer 3 - Network
- Switching and routing technologies, creating logical paths
- Transfers data from node to node.
- Routing and forwarding
- Addressing, internetworking, error handling, congestion control, package sequencing.

## Layer 2 - Data Link
- Data packates are encoded and decoded into bits
- Furnish transmission protocol knowledge and management 
- Handle errors in the physical layer, flow control and frame synchronization
- 2 sub layers:
  - MAC (Media Access Control): how a computer on the network gains access to the data and permission to transmit it.
  - LLC (Logical Link Control): control frame synchronization, flow control and error checking

## Layer 1 - Physical
- conveys the bit stream through th enetwork at the electrical and mechanical level.
- provides hardware.






