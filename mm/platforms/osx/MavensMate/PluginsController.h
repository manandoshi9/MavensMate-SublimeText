//
//  PluginsController.h
//  MavensMate
//
//  Created by Joseph on 3/22/13.
//  Copyright (c) 2013 Joseph. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import "AlertController.h"
#import "LoadingController.h"

@class LoadingController;

@interface PluginsController : NSWindowController <NSWindowDelegate> {
@private
    IBOutlet NSButton *sublimeTextInstallButton;
    IBOutlet NSProgressIndicator *sublimeTextButtonProgressIndicator;
    IBOutlet NSButton *sublimeTextBetaFlag;
}

@property (strong) NSString *foobarbat;

@property (strong) LoadingController *loadingController;
@property (strong) AlertController *alertController;

@property (strong) IBOutlet NSButton *sublimeTextBetaFlag;
@property (strong) IBOutlet NSButton *sublimeTextInstallButton;
@property (strong) IBOutlet NSProgressIndicator *sublimeTextButtonProgressIndicator;

-(PluginsController*)init;

@end

