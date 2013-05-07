//
//  AppDelegate.h
//  MavensMate
//
//  Created by Joseph on 9/5/12.
//  Copyright (c) 2012 Mavens. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import <WebKit/WebKit.h>

@interface AppDelegate : NSObject <NSApplicationDelegate>

@property (assign) IBOutlet WebView *webView;
@property (assign) IBOutlet NSWindow *window;
@property (assign) IBOutlet NSTextField *passedArguments;

@end
