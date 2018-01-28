.. raw:: html

    <h1>VSE_Transform_Tools</h1>
    <h2>Installation</h2>
    
    <ol>
    <li>Download the repository. Go to <a href="https://github.com/doakey3/VSE_Transform_Tools/releases">Releases</a> for a stable version, or click the green button above to get the most recent (and potentially unstable) version.</li>
    <li>Open Blender</li>
    <li>Go to File &gt; User Preferences &gt; Addons</li>
    <li>Click "Install From File" and navigate to the downloaded .zip file and install</li>
    <li>Check the box next to "VSE<em>Transform</em>Tools"</li>
    <li>Save User Settings so the addon remains active every time you open Blender</li>
    </ol>
    
    <h2>Operators</h2>
    <table>
        <tr>
            <td width=222px><a name="top_Add_Transform" href="#Add_Transform" title="Add transform modifier to
    selected strips">Add Transform</a></td>
            <td width=222px><a name="top_Crop" href="#Crop" title="Crop a strip in the Image
    Preview">Crop</a></td>
            <td width=222px><a name="top_Grab" href="#Grab" title="Change position of strips in
    Image Preview Window">Grab</a></td>
            <td width=222px><a name="top_Scale" href="#Scale" title="Scale strips in Image Preview
    Window">Scale</a></td>
        </tr>
        <tr>
            <td width=222px><a name="top_Adjust_Alpha" href="#Adjust_Alpha" title="Adjust alpha (opacity) of
    strips in the Image Preview">Adjust Alpha</a></td>
            <td width=222px><a name="top_Decrement_Pivot" href="#Decrement_Pivot" title="Changes the pivot mode">Decrement Pivot</a></td>
            <td width=222px><a name="top_Increment_Pivot" href="#Increment_Pivot" title="Changes the pivot mode">Increment Pivot</a></td>
            <td width=222px><a name="top_Select" href="#Select" title="Select visible sequences from
    the Image Preview">Select</a></td>
        </tr>
        <tr>
            <td width=222px><a name="top_Autocrop" href="#Autocrop" title="Collapse canvas to fit visible
    content">Autocrop</a></td>
            <td width=222px><a name="top_Delete" href="#Delete" title="Delete selected and their
    inputs recursively">Delete</a></td>
            <td width=222px><a name="top_Meta_Toggle" href="#Meta_Toggle" title="Toggle the Meta to reveal
    sequences within">Meta Toggle</a></td>
            <td width=222px><a name="top_Set_Cursor2D" href="#Set_Cursor2D" title="Set the pivot point location">Set Cursor2D</a></td>
        </tr>
        <tr>
            <td width=222px><a name="top_Call_Menu" href="#Call_Menu" title="Open keyframe insertion menu">Call Menu</a></td>
            <td width=222px><a name="top_Duplicate" href="#Duplicate" title="Duplicate selected and their
    inputs recursively">Duplicate</a></td>
            <td width=222px><a name="top_Rotate" href="#Rotate" title="Rotate strips in the Image
    Preview">Rotate</a></td>
            <td width=222px rowspan="1"></td>
        </tr>
    </table>
        <h3><a name="Add_Transform" href="#top_Add_Transform">Add Transform</a></h3>
    <p>A transform modifier must be added to a strip before the strip can 
    be grabbed, scaled, rotated, or cropped by this addon.
    Any strips with "Image Offset" enabled will transfer this offset to
    the transform strip</p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>T</kbd></td>
                <td>Add Transform</td>
                <td align="center" rowspan="1"><img src="https://i.imgur.com/v4racQW.gif" alt="Demo"></td>
            </tr>
        </table>
        <h3><a name="Adjust_Alpha" href="#top_Adjust_Alpha">Adjust Alpha</a></h3>
    <p></p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>Q</kbd></td>
                <td>Begin Alpha Adjusting</td>
                <td align="center" rowspan="8"><img src="https://i.imgur.com/PNsjamH.gif" alt="Demo"></td>
            </tr>
            <tr>
                <td align="center"><kbd>Ctrl</kbd></td>
                <td>Round to Nearest Tenth</td>
            </tr>
            <tr>
                <td align="center"><kbd>Right_Mouse</kbd></td>
                <td>Escape Alpha Adjust Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Esc</kbd></td>
                <td>Escape Alpha Adjust Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Left_Mouse</kbd></td>
                <td>Set Alpha, End Alpha Adjust Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Enter</kbd></td>
                <td>Set Alpha, End Alpha Adjust Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>0</kbd><kbd>1</kbd><kbd>2</kbd><kbd>3</kbd><kbd>4</kbd><kbd>5</kbd><kbd>6</kbd><kbd>7</kbd><kbd>8</kbd><kbd>9</kbd><kbd>.</kbd></td>
                <td>Set Alpha to Value Entered</td>
            </tr>
            <tr>
                <td align="center"><kbd>Alt</kbd><kbd>Q</kbd></td>
                <td>Set Alpha to 1.0</td>
            </tr>
        </table>
        <h3><a name="Autocrop" href="#top_Autocrop">Autocrop</a></h3>
    <p>Sets the scene resolution to fit all visible selected content in 
    the preview window without changing strip sizes.</p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>Shift</kbd><kbd>C</kbd></td>
                <td>Autocrop</td>
                <td align="center" rowspan="1"><img src="https://i.imgur.com/IarxF14.gif" alt="Demo"></td>
            </tr>
        </table>
        <h3><a name="Call_Menu" href="#top_Call_Menu">Call Menu</a></h3>
    <p>You may also enable automatic keyframe insertion.</p>
    
    <p><img src="https://i.imgur.com/kFtT1ja.jpg" alt="Automatic Keyframe Insertion" /></p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>I</kbd></td>
                <td>Call Menu</td>
                <td align="center" rowspan="1"><img src="https://i.imgur.com/9Cx6XKj.gif" alt="Demo"></td>
            </tr>
        </table>
        <h3><a name="Crop" href="#top_Crop">Crop</a></h3>
    <p></p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>C</kbd></td>
                <td>Begin/Set Cropping, Add Transform if Needed</td>
                <td align="center" rowspan="5"><img src="https://i.imgur.com/k4r2alY.gif" alt="Demo"></td>
            </tr>
            <tr>
                <td align="center"><kbd>Esc</kbd></td>
                <td>Escape Crop Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Left_Mouse</kbd></td>
                <td>Click Handles to Drag</td>
            </tr>
            <tr>
                <td align="center"><kbd>Enter</kbd></td>
                <td>Set Crop, End Grab Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Alt</kbd><kbd>C</kbd></td>
                <td>Uncrop</td>
            </tr>
        </table>
        <h3><a name="Decrement_Pivot" href="#top_Decrement_Pivot">Decrement Pivot</a></h3>
    <p>Changes how strips are rotated and scaled. (sets the point of 
    origin).</p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>Comma</kbd></td>
                <td>Decrement Pivot</td>
                <td align="center" rowspan="1"><img src="https://i.imgur.com/3ru1Xl6.gif" alt="Demo"></td>
            </tr>
        </table>
        <h3><a name="Delete" href="#top_Delete">Delete</a></h3>
    <p>Deletes all selected strips as well as any strips that are inputs
    of those strips.
    For example, deleting a transform strip with this operator will
    also delete the strip it was transforming.</p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>Del</kbd></td>
                <td>Delete</td>
                <td align="center" rowspan="1"><img src="https://i.imgur.com/B0L7XoV.gif" alt="Demo"></td>
            </tr>
        </table>
        <h3><a name="Duplicate" href="#top_Duplicate">Duplicate</a></h3>
    <p>Duplicates all selected strips and any strips that are inputs
    of those strips.
    Calls the Grab operator immediately after duplicating.</p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>Shift</kbd><kbd>D</kbd></td>
                <td>Duplicate</td>
                <td align="center" rowspan="1"><img src="https://i.imgur.com/IJh7v3z.gif" alt="Demo"></td>
            </tr>
        </table>
        <h3><a name="Grab" href="#top_Grab">Grab</a></h3>
    <p></p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>G</kbd></td>
                <td>Begin Moving, Add Transform if Needed</td>
                <td align="center" rowspan="11"><img src="https://i.imgur.com/yQCFI0s.gif" alt="Demo"></td>
            </tr>
            <tr>
                <td align="center"><kbd>Shift</kbd></td>
                <td>Hold to Enable Fine Tuning</td>
            </tr>
            <tr>
                <td align="center"><kbd>Ctrl</kbd></td>
                <td>Hold to Enable Snapping</td>
            </tr>
            <tr>
                <td align="center"><kbd>Right_Mouse</kbd></td>
                <td>Escape Grab Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Esc</kbd></td>
                <td>Escape Grab Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Left_Mouse</kbd></td>
                <td>Set Position, End Grab Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Enter</kbd></td>
                <td>Set Position, End Grab Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>0</kbd><kbd>1</kbd><kbd>2</kbd><kbd>3</kbd><kbd>4</kbd><kbd>5</kbd><kbd>6</kbd><kbd>7</kbd><kbd>8</kbd><kbd>9</kbd><kbd>.</kbd></td>
                <td>Set Position by Value Entered</td>
            </tr>
            <tr>
                <td align="center"><kbd>X</kbd><kbd>Y</kbd></td>
                <td>Constrain Grabbing to Respective Axis</td>
            </tr>
            <tr>
                <td align="center"><kbd>Middle_Mouse_Button</kbd></td>
                <td>Constrain Grabbing to Axis</td>
            </tr>
            <tr>
                <td align="center"><kbd>Alt</kbd><kbd>G</kbd></td>
                <td>Set Position to [0, 0]</td>
            </tr>
        </table>
        <h3><a name="Increment_Pivot" href="#top_Increment_Pivot">Increment Pivot</a></h3>
    <p>Changes how strips are rotated and scaled. (sets the point of 
    origin).</p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>Period</kbd></td>
                <td>Increment Pivot</td>
                <td align="center" rowspan="1"><img src="https://i.imgur.com/3ru1Xl6.gif" alt="Demo"></td>
            </tr>
        </table>
        <h3><a name="Meta_Toggle" href="#top_Meta_Toggle">Meta Toggle</a></h3>
    <p>Toggles the selected strip if it is a META. If the selected strip is 
    not a meta, recursively checks inputs until a META strip is 
    encountered and toggles it. If no META is found, this operator does 
    nothing.</p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>Tab</kbd></td>
                <td>Meta Toggle</td>
                <td align="center" rowspan="1"><img src="https://i.imgur.com/ya0nEgV.gif" alt="Demo"></td>
            </tr>
        </table>
        <h3><a name="Rotate" href="#top_Rotate">Rotate</a></h3>
    <p></p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>R</kbd></td>
                <td>Begin Rotating, Add Transform if Needed</td>
                <td align="center" rowspan="9"><img src="https://i.imgur.com/SyL2HeA.gif" alt="Demo"></td>
            </tr>
            <tr>
                <td align="center"><kbd>Shift</kbd></td>
                <td>Hold to Enable Fine Tuning</td>
            </tr>
            <tr>
                <td align="center"><kbd>Ctrl</kbd></td>
                <td>Hold to Enable Stepwise Rotation</td>
            </tr>
            <tr>
                <td align="center"><kbd>Right_Mouse</kbd></td>
                <td>Escape Rotate Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Esc</kbd></td>
                <td>Escape Rotate Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Left_Mouse</kbd></td>
                <td>Set Rotation, End Rotate Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Enter</kbd></td>
                <td>Set Rotation, End Rotate Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>0</kbd><kbd>1</kbd><kbd>2</kbd><kbd>3</kbd><kbd>4</kbd><kbd>5</kbd><kbd>6</kbd><kbd>7</kbd><kbd>8</kbd><kbd>9</kbd><kbd>.</kbd></td>
                <td>Set Rotation to Value Entered</td>
            </tr>
            <tr>
                <td align="center"><kbd>Alt</kbd><kbd>R</kbd></td>
                <td>Set Rotation to 0 Degrees</td>
            </tr>
        </table>
        <h3><a name="Scale" href="#top_Scale">Scale</a></h3>
    <p></p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>S</kbd></td>
                <td>Begin Scaling, Add Transform if Needed</td>
                <td align="center" rowspan="11"><img src="https://i.imgur.com/oAxSEYB.gif" alt="Demo"></td>
            </tr>
            <tr>
                <td align="center"><kbd>Shift</kbd></td>
                <td>Enable Fine Tuning</td>
            </tr>
            <tr>
                <td align="center"><kbd>Ctrl</kbd></td>
                <td>Enable Stepwise scaling</td>
            </tr>
            <tr>
                <td align="center"><kbd>Right_Mouse</kbd></td>
                <td>Escape Scale Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Esc</kbd></td>
                <td>Escape Scale Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Left_Mouse</kbd></td>
                <td>Set Scale, End Scale Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>Enter</kbd></td>
                <td>Set Scale, End Scale Mode</td>
            </tr>
            <tr>
                <td align="center"><kbd>0</kbd><kbd>1</kbd><kbd>2</kbd><kbd>3</kbd><kbd>4</kbd><kbd>5</kbd><kbd>6</kbd><kbd>7</kbd><kbd>8</kbd><kbd>9</kbd><kbd>.</kbd></td>
                <td>Set Scale by Value Entered</td>
            </tr>
            <tr>
                <td align="center"><kbd>X</kbd><kbd>Y</kbd></td>
                <td>Constrain Scaling to Respective Axis</td>
            </tr>
            <tr>
                <td align="center"><kbd>Middle_Mouse_Button</kbd></td>
                <td>Constrain Scaling to Axis</td>
            </tr>
            <tr>
                <td align="center"><kbd>Alt</kbd><kbd>S</kbd></td>
                <td>Unscale</td>
            </tr>
        </table>
        <h3><a name="Select" href="#top_Select">Select</a></h3>
    <p></p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>Right_Mouse</kbd></td>
                <td>Select Visible Strip</td>
                <td align="center" rowspan="3"><img src="https://i.imgur.com/EVzmMAm.gif" alt="Demo"></td>
            </tr>
            <tr>
                <td align="center"><kbd>Shift</kbd></td>
                <td>Enable Multi Selection</td>
            </tr>
            <tr>
                <td align="center"><kbd>A</kbd></td>
                <td>Toggle Selection</td>
            </tr>
        </table>
        <h3><a name="Set_Cursor2D" href="#top_Set_Cursor2D">Set Cursor2D</a></h3>
    <p>Set the pivot point (point of origin) location. This will affect 
    how strips are rotated and scaled.</p>
    
        <table>
            <tr>
                <th width=208px>Shortcut</th>
                <th width=417px>Function</th>
                <th width=256px>Demo</th>
            <tr>
                <td align="center"><kbd>Left_Mouse</kbd></td>
                <td>Cursor 2D to mouse position</td>
                <td align="center" rowspan="2"><img src="https://i.imgur.com/1uTD9C1.gif" alt="Demo"></td>
            </tr>
            <tr>
                <td align="center"><kbd>Ctrl</kbd><kbd>Left_Mouse</kbd></td>
                <td>Snap Cursor 2D to nearest strip corner or mid-point</td>
            </tr>
        </table>