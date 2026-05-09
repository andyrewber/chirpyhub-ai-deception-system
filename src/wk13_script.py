'''

Traps and Decoys - Week 13

'''

'''
---------------------------------------------------
Scenario:

ChirpyHub wants to harden its servers by implementing decoy directories.
The directories would serve as decoys against malicious actors and provide
notifications to system admins (traps) to indicate there has been unexpected access.

---------------------------------------------------

Before Starting:

Please review:
    - All the material in this repository
    - The examples in the examples folder
    - Attached material in D2L
    - Make sure you thoroughly understand what each example is doing.

---------------------------------------------------

Task:

Important Note: In order to receive credit for this assignment 
you MUST have completed ALL the exercises and submitted them on time
(by the end of each week unless otherwise noted in D2L) 
in the Traps and Decoys section in D2L.

### Part 1 Sketch ###

Sketch you decoy directory using paper and pencil or a tool of your choice

General Information:
- Sketch the decoy directory structure for ChirpyHub
- Items you may want to include would be files that may entice malicious actors.
- Some items you could consider
    - Plain text passwords
    - Salary information
    - Workstation notes
    - Database dumps
- Work on including realistic items in your directory.
- Ideally use a variety of file types: csvs, texts, docx, etc. 

More specifically: 

- There will be 2 directories
    - One Directory Structure will be for a workstation
    - One will be for an internal application server.
    - name them workstation/ and server/
    
 - Each directory must contain:
    - At least 3 subdirectories with at least 2 files each.
     (You can do more to make it more believable)
    - Files that have realistic names and content.
     - Some ideas can be:
         - budget.txt
         - employee_notes.txt
         - config.cfg
         - access_logs.txt
         - event_logs.txt
         - passwords.txt
         - deleted_chirps.csv
         - confidential_chirps.csv
         
 - The initial file contents do not need to be extensive, but they should appear believable.
 - You should, however, be able to create csvs, txt, bin, config files using the tools we've worked with in class.  
 - The focus here is making this look BELIEVABLE.
 

- Your final sketch should be submitted in the docs/ folder.
     
#### PART 2 SCRIPT DEVELOPMENT ####

You will use the examples as a baseline.

Create the following scripts in the src/ folder:

# Script 1: (decoy_structure.py)

Turn your sketch into decoy directories programmatically. 


1) Create two decoy directory structures under a folder called decoys/ in the docs/ folder.
 So docs/decoys/workstation/ and docs/decoys/server/
 
    - You are not expected to programmatically create more complex files like docx or xlsx etc.
    - You may either create these manually and indicate so in your script comments
    - Or you may use AI Assistance to build the more complex files - make sure you cite this and link your conversation.

2) After creating the structure, take an initial "known state" snapshot:
     - Record the metadata (atime, mtime, ctime, size, mode) for every file.
     - Save this snapshot to docs/known_state.json using Python's json module or to a csv if you prefer.
     - Pretty table can be used to export to either (review the examples)

# Script 2: (dynamic_activity.py)

1) Draw inspiration from examples/meta_mod.py to build a script that simulates
   realistic file system activity across your decoy directories.

2) Your script must include at least the following types of simulated activity:
     a) Timestamp modification (atime and/or mtime) using os.utime
     b) File content modification (append or change a line in at least one file per run)
     c) File size change (content additions should cause a measurable size difference)

3) Activity must appear realistic:
     - Use time-of-day logic: 
            - Maybe changes should only occur during "work hours" (e.g., 8 AM - 6 PM)?
     - Use day-of-week logic: distinguish between weekday and weekend behavior.
            - Maybe changes to some files only happen on weekdays and exclude holidays?
     - Use randomization to vary which files are touched each run so the pattern
       is not perfectly uniform. random.choice or random.sample can work well here.
    - Make changes believable:
        - add realistic logs
        - add realistic notes
        - add realistic info
        - Maybe create a pool of things to add and select one
    (You are not expected to edit the more complex file types like docx, etc here but you must edit at least 5 of your files)
       
4) After each simulated activity cycle, update the known_state.json /csv snapshot
   to reflect the new "known good" state of the decoy vault.

5) Display a PrettyTable summary after each run showing:
     - Which files were modified
     - What type of change was made (timestamp, content, or both)
     - The new mtime value

# Script 3: (activity_log.py)

1) Create a companion script that appends each
   activity cycle's results to a log file: docs/activity_log.txt

2) Each log entry should include:
     - A timestamp of when the activity script ran
     - Which files were modified
     - What change was applied
     - The resulting new metadata value (e.g., mtime after update)

3) The log format should be human-readable — plain text with clear labels is fine.

# Script 4: (trap_demo.py)

Take inspiration from the directory_watcher.py to watch your directories for changes.

Each trap must log or alert when the following events occur.
 - File opened
 - File altered
 - File deleted
 - New file added

Demonstrate all four in your video.

---------------------------------------------------

Submission Considerations:

- Screenshot every output (PrettyTable summaries and log entries)
- Run your dynamic_activity.py at least 3 times and include all 3 output screenshots.
- Show the changes to files that are believable.
- Your known_state.json/csv should be committed in its final state.
- The activity_log.txt should reflect all the runs.
- AI Usage is only approved for building complex files
- In a pinch, you may use AI for assistance populating files with believable content.
- Though make sure you populate at least one on your own.
- The rest of the scripts should be developed by you using the examples as inspiration.
- The course AI Usage Policy applies to everything else.

---------------------------------------------------

To Submit:
    - Commit and Push your final scripts to GitHub.
    - Commit and push legible screenshots of your results to the /docs/ folder.
        - All script runs must be visible.
        - File names, modification types, and timestamps must be readable.
        - The updated known_state.json/csv and activity_log.txt must be committed.
    
    Video Walkthrough:

    - Record a short video (5-10 minutes) that walks through all four steps.
    - This is a multi-week project — your video should cover the full picture:
     - Step 1: Walk through your decoy directories and explain your design choices.
     - Step 2: Show dynamic activity running; show timestamps that look real.
     - Step 3: Show the monitoring script running and the log updating live.
     - Step 4: Demonstrate all four trap events and their log entries.
     
    Provide a small narration explaining the most significant findings that
    you reviewed in your reflection.
     
    If your video is too large for GitHub, submit your video to D2L.
    A screen recording with your narration is fine.

   Reflection:

    Add a reflection.md file in the docs/ folder and:
     - Describe how you designed your activity schedule (time-of-day, day-of-week logic).
     - What human behavior patterns did you model? Where did you find information on them?
     - What determines whether a metadata change looks "natural" to a forensic investigator?
     - How would you detect that?
     - Would a Machine Learning model help schedule decoy activity more realistically,
       or is structured randomization sufficient? Why?
     - If an attacker reads a file in your decoy vault, which metadata field changes?
     - Explain what makes a metadata change "convincing" vs. obviously synthetic.
     - Identify one limitation of your current approach that an attacker or analyst
       could exploit to detect that the activity is scripted.
     - Cite any outside assistance you had.
       If no work is cited, you attest that ALL work submitted is originally yours.
     - As a guideline, your reflection should be between 300-500 words.

'''
