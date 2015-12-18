# Pi-Chair
Weight tracker using Raspberry Pi and Ultrasonic range finder


It uses Raspberry Pi and ultrasonic range finder to detect the changes in weight of a person over a period of time. To achieve this, the ultrasonic range finder was attached onto the chair arm where it could send/receive ultrasonic impulses to/from the ground. When someone sits on the chair, the process is triggered. It range-finder starts sending quick impulses at a certain rate thus enabling me to calculate the speed at which the chair is descending to get an estimate of the person's weight. Using Google SpreadSheet API, I enabled it to upload the data directly to a Google Spreadsheet which can be used to visualize the changes.
