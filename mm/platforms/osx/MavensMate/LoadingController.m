//
//  LoadingController.m
//  MavensMate
//
//  Created by Joseph on 3/22/13.
//  Copyright (c) 2013 Joseph. All rights reserved.
//

#import "LoadingController.h"

@implementation LoadingController

-(LoadingController*)init {
	self = [[LoadingController alloc] initWithWindowNibName:@"Loading"];
    [self.window setDelegate:self];
    [self.window setLevel:kCGMainMenuWindowLevel-2];
    [self.window setCollectionBehavior:NSWindowCollectionBehaviorStationary|NSWindowCollectionBehaviorCanJoinAllSpaces|NSWindowCollectionBehaviorFullScreenAuxiliary];
    //[self.window makeKeyAndOrderFront:self];
    self = [super init];
    if (self) {
        //Initialization code goes here
    }
    return self;
}

-(void) show {
    NSLog(@"showing loading!!");
    [_loadingBar startAnimation:self];
    [NSApp activateIgnoringOtherApps:YES];
    [_loadingWindow makeKeyAndOrderFront:nil];
}

-(void) hide {
    [_loadingBar stopAnimation:self];
    [_loadingWindow close];
}

@end
