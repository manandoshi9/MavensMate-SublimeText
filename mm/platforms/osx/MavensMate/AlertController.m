//
//  AlertController.m
//  MavensMate
//
//  Created by Joseph on 3/22/13.
//  Copyright (c) 2013 Joseph. All rights reserved.
//

#import "AlertController.h"

@implementation AlertController

@synthesize alertMessage = _alertMessage;

-(AlertController*)init {
	self = [[AlertController alloc] initWithWindowNibName:@"Alert"];
    [self.window setDelegate:self];
    [self.window setLevel:kCGMainMenuWindowLevel-1];
    [self.window setCollectionBehavior:NSWindowCollectionBehaviorStationary|NSWindowCollectionBehaviorCanJoinAllSpaces|NSWindowCollectionBehaviorFullScreenAuxiliary];
    //[self.window makeKeyAndOrderFront:self];
    self = [super init];
    if (self) {
        //Initialization code goes here
    }
    return self;
}

-(void)showWithMessage:(NSString*)message {
    [NSApp activateIgnoringOtherApps:YES];
    [_alertMessage setStringValue:message];
    [_alertWindow makeKeyAndOrderFront:nil];
}

-(void) show {
    [NSApp activateIgnoringOtherApps:YES];
    [_alertWindow makeKeyAndOrderFront:nil];
}

-(IBAction) close:(id)sender {
    [_alertWindow close];
}

-(void) hide {
    [_alertWindow close];
}

@end
