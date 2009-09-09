/*
    This class is a basic extension of the Applet class.  It would generally
    be used as the main class with a Java browser or the AppletViewer.  But
    an instance can be added to a subclass of Container.  To use this applet
    with a browser or the AppletViewer, create an html file with the
    following code:

    <HTML>
    <HEAD>
    <TITLE> Echo </TITLE>
    </HEAD>
    <BODY>

    <APPLET CODE="Echo.class" WIDTH=283 HEIGHT=190></APPLET>

    </BODY>

    </HTML>

    You can add controls to Echo with Cafe Studio.
    (Menus can be added only to subclasses of Frame.)
 */

import java.awt.*;
import java.applet.*;

public class Echo extends Applet {
    public void init() {

        super.init();

        java.net.URL codebase = getCodeBase();

        //{{INIT_CONTROLS
        setLayout(new BorderLayout());
	// resize(283,190);
        label1=new Label(codebase.toString(), Label.CENTER);
        add("Center", label1);
        //}}
    }

    public boolean handleEvent(Event event) {
        return super.handleEvent(event);
    }

    //{{DECLARE_CONTROLS
    Label label1;
    //}}
}
