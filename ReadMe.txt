*In this folder
\CXX\					Folders containing for each measurement the measured RedFox, MTS and DIC data
ReadMe.txt				This file
overview.xlsx				Excel file showing an overview of all the SENB tests with the relevant test parameters
AnalyseCruciform.py			Python file for reading and analysing the RedFox data for specimens SA1b, SA4, SA5, SA6, SB1, SC1, SC2, SC3
Specimens_infoCruciforms.py		Python file containing for each run a number of parameters for doing the data analysis
CompareCruciform.py			Python file for comparing multiple strips from different tests
ServiceComm V4.25_Cruciform_XX.xlsx	Excel file used for acquiring the RedFox RFV2.202100XX data
Draft Results Cruciforms.docx		Word document containing draft plots for the executed tests

*Nomenclenture
C => Cruciform
A/B/C => A=Fully welded, B=Fillet weld, C=Partially welded

*Analysis
AnalyseCruciform.py calculates for each sensor strip:
LMV = local magnetic variation between sensor i and i+1 with respect to a reference measurement at the start
LMV2 = local magnetic variation between sensor i and i+2 with respect to a reference measurement at the start
Norm = norm of vectorial change between the current field and a reference state at the start

*Specimen Logbook
*11-01-22
CA1		Failure at 230 000 cycles

*12-01-22
CB1		Failure at 128 000 cycles

*13-01-22
CA2 (X) 	3M cycles of prefatigueing

*17-01-22
CA2b		Failure at 2 336 690 cycles +3M cycles

*21-01-22
CB2		Failure at 600 000 cycles

*24-01-22
CC1		Failure at 71 004 cycles
CA3-pre		No failure, 250 000 cycles

*25-01-22
CA4-pre		No failure, 250 000 cycles
CC2		Failure at cycles

*26-01-22
CB3-pre		No failure, 250 000 cycles
CB4-pre		No failure, 250 000 cycles

*27-01-22
CC3-pre		No failure, 250 000 cycles

*28-01-22
CC4 (X)		No failure

*31-01-22
CB3		Failure at 212 000 + 250 000 cycles		
CB4		Failure at 148 000 + 250 000 cycles

*01-02-22
CA3		Failure at 148 000 + 250 000 cycles

*02-02-22
CA4		Failure at 240 000 + 250 000 cycles

*03-02-22
CB5		Failure at 167 419 cycles
CC4b		Failure at 600 000 + 1.8M cycles