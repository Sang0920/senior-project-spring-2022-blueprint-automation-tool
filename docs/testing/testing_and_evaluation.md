<!--
File:         testing_and_evaluation.md
Description:  Describes how code was validated so that everything works
-->

# Testing and Evaluation

## Functionality Tests

To ensure that Project B.A.T. is functionally correct in its operations and use cases, testing was
conducted using different use cases of each functionality of the program.

### Settings

Settings were tested to make sure that any setting that was changed by the user would save as soon
as the program shut down normally or due to unexpected crashes. Settings were also tested by
intentionally changing the settings file to invalid errors manually, such as deleting all of the
contents of the file or deleting the config.yml file.

### Automation

Automation was tested extensively throughout development to ensure that the program was able to
stably run and manipulate the Minecraft environment. Tests were designed to push the program (and
the game) to its limits, ensuring that the program was able to perform under pressure. These
conditions included running the program with:

- a large amount of places loaded into the program at once
- large scale builds in the world
- places that required far distances of travel

As a failsafe, the program implements a emergency shutdown feature that will stop any automation as
soon as it is safe to do so. To trigger this failsafe, the user just needs to hold down the "END"
key on their keyboard.

### User Interface

Similarly to the automation feature of the game, the user interface was tested with stress tests to
ensure stability. These tests include:

- Loading a large amount of places to build in the program at the same time.
- Continuously changing the settings of the program to make sure that the program gave live updates
  to the settings
- Trying to start the automation with places loaded to build
- Trying to start the automation with no reference point loaded
- Trying to start the automation when Minecraft was not loaded into a world
- Trying to detect the game version when no version of the game was currently running
- Resetting the program to its default settings multiple times

In addition to these tests, the user interface also has an alert feature built into it that will
give the user a pop-up alert message whenever an unresolvable error occurs. This alert will
notifies the user what went wrong and how to fix the error, allowing for built-in troubleshooting.

## Unit Tests

Helper functions to the core functionalites of the program were also tested using unit testing and
the pytest module to ensure that basic computations and translations were working as expected. These
basic modules that are used multiple times throughout the program and were tested with unit testing
were:

- The color_matcher.py module
- The place_parser.py module
- The settings.py module

## Debugging Functionality

In addition to the above tests, the program has been implemented with debugging logs available for
greater debugging of the executable file. The logs are stored in a log file in the
`Documents/Project BAT/logs` folder. These files contain all the console logs for each application run
to help debug what went wrong in the case that the execution of the program goes wrong.
