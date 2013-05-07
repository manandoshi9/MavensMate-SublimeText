//
//  AboutController.m
//  MavensMate
//
//  Created by Joseph on 3/25/13.
//  Copyright (c) 2013 Joseph. All rights reserved.
//

#import "AboutController.h"

@implementation AboutController

@synthesize versionNumber = _versionNumber;

-(AboutController*)init {
	self = [[AboutController alloc] initWithWindowNibName:@"About"];
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

- (void)windowDidLoad {
    NSString *versionNumber =[[[NSBundle mainBundle] infoDictionary] valueForKey:@"CFBundleVersion"];
    NSString *versionLabel = [@"Version " stringByAppendingString:versionNumber];
    [_versionNumber setStringValue:versionLabel];
}



@end
