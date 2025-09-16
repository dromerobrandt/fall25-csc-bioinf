# Introduction
This is Assignment1's week 1 report. It is a reflection on the steps I took during the assignment and what I think I can improve upon for next assignment. For this first assignment, I got stuck multiple times due to technicle issues and felt way in the weeds. I believe that is because I was trying to set everything up and felt a bit rusty, since it is the beginning of the term.

# Preliminaries
I began by installing the miniconda and set up the bioinfo environment, followed by the Codon installation. This part was quite straightforward, but I had to install some other prerequisites since I changed my operating system not long ago.

# Setting up the repository
Next, I had to set up my GitHub repository. This took a while because I don't find setting up new GitHub repositories straightforward and needed a reminder of how to do it. I also had to set up the CI, which had a couple issues: the indentation was wrong because I copy and pasted it, and "Name" was capitalized at the top. Those were easily detected, so they didn't delay my assignment much.

# Deliverable
The goals of this assignment were to gain familiarity with software development methods and automation, such as GitHub CI, project structure, and automating results; gain familiarity with Codon; and reproduce previously published results.

## Cloning and reproducing
Getting into the meaty part of the assignment, I proceeded to clone Zhongyu Chen's GitHub repository (https://github.com/zhongyuchen/genome-assembly?tab=readme-ov-file) and ran all the experiments with Python. This was strightforward, but I was not very sure what to do with the output to reproduce the results until it was updated that only N50 should be reproduced. I had to look up what N50 was, but it resulted in a strightforward calculation.

## Converting to Codon
I then had to convert the Python code to Codon. Originally, I thought I could just run Codon, but that was not true; some errors popped up, which I had to work with to actually convert the .py file to something Codon compatible. It turns out that Codon does support the os and sys libraries, but not completely. The os.path.join and sys.setrecursionlimit do not work with Codon. I am not sure why os.path.join didn't work, but the sys.setrecursionlimit did not work because Codon is compiled and executed, not simply interpreted like Python. The os.path.join had a quick fix, but the sys.setrecursionlimit did not, which required me to revise the _get_depth() method. I also had to provide additional type hints to make dbg.py work with Codon.

## Writing the script
Lastly, I had to write a script that would run the Python code and Codon code automatically, compile the results and runtimes, and output the comparison on stdout. This wasn't very tedious, but it took some time because I had to learn a bit of Bash to get it done. After some revision on the formatting, I finished the assignment.

# Last thoughts
A few things went awry during this assignment, which I learned about and expect to avoid them in upcoming ones. I also filled out ai.txt and report.md at the end of the assignment, which was a mistake, because I forgot about some other stuff that I encountered. I will make sure to update more regularly, at the end of every session I have with the assignment.
