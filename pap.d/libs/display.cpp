//////////////////////////////////////////////
// Author: Artur Z. (HUSKI3)                //
// Date:   25/3/21                          //
// Github: https://github.com/HUSKI3        //
// File:   display.cpp (Library)            //
//////////////////////////////////////////////
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <X11/Xlib.h>
#include <X11/extensions/Xrandr.h>

void printMonitorInfo()
{
    Display * display = XOpenDisplay( nullptr );
    if (!display)
    {
        std::cout << "cannot open X Display" << std::endl;
        return;
    }

    int dummy1, dummy2;
    int major, minor;
    if (!XRRQueryExtension( display, &dummy1, &dummy2 )
     || !XRRQueryVersion( display, &major, &minor ))
    {
        std::cout << "failed to retrieve XRandR version" << std::endl;
        XCloseDisplay( display );
        return;
    }

    if (major <= 1 && minor < 5)
    {
        std::cout << "RandR version at least 1.5 is required" << std::endl;
        XCloseDisplay( display );
        return;
    }

    Window rootWindow = RootWindow( display, DefaultScreen( display ) );

    Bool onlyActive = false;  // if set it returns only active monitors (non-0x0 monitors)
    int monitorCnt;
    XRRMonitorInfo * xMonitors = XRRGetMonitors( display, rootWindow, onlyActive, &monitorCnt );
    if (!xMonitors)
    {
        std::cout << "failed to retrieve monitor info" << std::endl;
        XCloseDisplay( display );
        return;
    }

    for (int monitorIdx = 0; monitorIdx < monitorCnt; monitorIdx++)
    {
        std::cout
            << "Output name: " << XGetAtomName( display, xMonitors[ monitorIdx ].name )
            << ", width: " << xMonitors[ monitorIdx ].width
            << ", height: " << xMonitors[ monitorIdx ].height
            << ", primary: " << xMonitors[ monitorIdx ].primary
            << std::endl;
    }

    XCloseDisplay( display );
}
