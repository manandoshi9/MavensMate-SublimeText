//
//  AppDelegate.m
//
//  Created by Joseph Ferraro on 2/23/12.
//  Copyright (c) 2013 Julian Meyer. All rights reserved.
//

#import "AppDelegate.h"
#import "StatusMenuController.h"


@implementation AppDelegate

@synthesize menuController = _menuController;

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification {
    //[self setupDefaults];
    _menuController = [[StatusMenuController alloc] init];
	[NSBundle loadNibNamed:@"StatusMenu" owner:_menuController];
    [self startServer];
}

- (void)setupDefaults {
    // future functionality
    //[[[NSUserDefaultsController sharedUserDefaultsController] values] setValue:[NSNumber numberWithBool:YES]
    //                                  forKey:@"stBeta"];
}


//**********************************
//** local server related actions **
//**********************************

-(IBAction) restartServer:(id)sender {
    [self stopServer];
    [self startServer];
}

-(void) stopServer {
    system("killAll mmserver");
}

-(void)applicationWillTerminate:(NSNotification *)notification {
    [self stopServer];
}

-(void) startServer {
    [self performSelectorInBackground:@selector(startServerInBackground) withObject:nil];
}

-(void) startServerInBackground {
    @try {
        NSBundle*mainBundle=[NSBundle mainBundle];
        NSTask *task;
        task = [[NSTask alloc] init];
        NSString*mmpath=[mainBundle pathForResource:@"mm" ofType:(nil) inDirectory:(@"mm")];
        NSString*mmserverpath=[mainBundle pathForResource:@"mmserver" ofType:(nil) inDirectory:(@"mmserver")];
        
        [task setLaunchPath: mmserverpath];
        
        NSArray *arguments;
        arguments = [NSArray arrayWithObjects: @"-m", mmpath, nil];
        [task setArguments: arguments];
        
        NSPipe *pipe;
        pipe = [NSPipe pipe];
        [task setStandardOutput: pipe];
        
        
        NSFileHandle *file;
        file = [pipe fileHandleForReading];
        
        [task launch];
        
        // need to rework this to be non-blocking
        //    NSData *data;
        //    data = [file readDataToEndOfFile];
        //
        //    NSString *string;
        //    string = [[NSString alloc] initWithData: data encoding: NSUTF8StringEncoding];
        //    NSLog (@"grep returned:\n%@", string);
        
        //[string release];
        //return string;
        //[task release];
    }
    @catch (NSException *e) {
        NSLog(@"Server failed to start: %@", e);
    }
}


@end