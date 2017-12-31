.. image:: https://i.imgur.com/PzGmbrj.png

.. contents::

Installation
============
1. Download the repository. (click the green button above that says
   "Clone or Download")
2. Open Blender_.
3. Go to File > User Preferences > Addons
4. Click "Install From File" and navigate to the downloaded zip file and
   install.
5. Check the box next to "VSE_Transform_Tools"
6. Save User Settings so the addon remains active every time you open Blender_

.. _Blender: https://www.blender.org

Usage
=====
Keyboard Shortcut Summary
-------------------------
:T:       Add Transform Modifier
:G:       Grab Strip
:S:       Scale Strip
:R:       Rotate Strip
:Q:       Modify Opacity
:C:       Crop
:I:       Insert Keyframe
:Shift+C: Collapse Canvas
:Alt+G:   Set Strip Position to Zero
:Alt+S:   Set Strip Scale to One
:Alt+R:   Set Strip
:Alt+Q:   Set Opacity to One
:Alt+C:   Set Crops to Zero

Selecting
---------
Strips may be selected in the preview window by right clicking. Hold the
**Shift** key to toggle the selection of multiple strips.

Fine Tuning & Snapping
----------------------
When Grabbing, Rotating, or Scaling, hold the **Shift** key to fine tune
movement, or hold the **Ctrl** key to snap movement.

Exact Input
-----------
When Grabbing, Rotating, Scaling, or Modifying Opacity, you can enter
specific values using your keyboard. For example, entering: **R**,
**3**, **0**, **.**, **5** will rotate the selected strip 30.5 degrees.

Examples
--------
Grab
~~~~

Scale
~~~~~

Rotate
~~~~~~

Opacity
~~~~~~~

Crop
~~~~

Insert Keyframe
~~~~~~~~~~~~~~~

Collapse Canvas
~~~~~~~~~~~~~~~

Todo
====
* |-| Change anchor mode with < and > keys
* |-| Icon that displays changed anchor position
* |-| Enable Mouse to loop back when adjusting beyond Blender window
* |-| Scaling on canvas x & y axis
* |-| Duplicate strip with Shift+D
* |-| Delete strip with Delete key
* |-| Code Cleanup (replace global variables with Blender Props)

.. |+| unicode:: U+2611
.. |-| unicode:: U+2610
