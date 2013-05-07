//
//  AppDelegate.m
//  MavensMate
//
//  Created by Joseph on 9/5/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "AppDelegate.h"

@implementation AppDelegate


@synthesize window;
@synthesize webView;
@synthesize passedArguments;

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    
    NSLog(@"process info: %@", [[NSProcessInfo processInfo] arguments]);
    passedArguments.stringValue = [[[NSProcessInfo processInfo] arguments] objectAtIndex:2];
    NSString *file_location = [[[NSProcessInfo processInfo] arguments] objectAtIndex:2];
    //NSString *file_location = @"/Users/josephferraro/Downloads/Mavens Home/team.htm";
    self.webView.mediaStyle = @"screen";
    self.webView.customUserAgent = @"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10";
    self.webView.preferences.autosaves = false;
    self.webView.preferences.shouldPrintBackgrounds = true;
    self.webView.preferences.javaScriptCanOpenWindowsAutomatically = true;
    self.webView.preferences.allowsAnimatedImages = false;
    self.webView.mainFrame.frameView.allowsScrolling = true;
    self.webView.frameLoadDelegate = self;
    NSString *htmlContents = [NSString stringWithContentsOfFile:file_location
                                                       encoding:NSUTF8StringEncoding
                                                          error:NULL];
    NSURL *file_url = [NSURL fileURLWithPath:file_location];
    [[self.webView mainFrame] loadHTMLString:htmlContents baseURL:file_url];
}

- (BOOL)applicationShouldTerminateAfterLastWindowClosed:(NSApplication *)theApplication {
    return YES;
}

@end
