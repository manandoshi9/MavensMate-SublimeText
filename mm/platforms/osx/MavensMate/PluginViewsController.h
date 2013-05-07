//
//  PluginViewsController.h
//  MavensMate
//
//  Created by Joseph on 3/30/13.
//  Copyright (c) 2013 Joseph. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import "DBPrefsWindowController.h"
#import "AlertController.h"
#import "LoadingController.h"

@interface PluginViewsController : DBPrefsWindowController {
    IBOutlet NSButton *st2InstallButton;
    IBOutlet NSButton *st3InstallButton;
    
    IBOutlet NSProgressIndicator *st2ButtonLoading;
    IBOutlet NSProgressIndicator *st3ButtonLoading;
}

@property (strong, nonatomic) IBOutlet NSView *sublimeText2View;
@property (strong, nonatomic) IBOutlet NSView *sublimeText3View;
@property (strong, nonatomic) IBOutlet NSView *futurePluginView;


@property (strong) LoadingController *loadingController;
@property (strong) AlertController *alertController;

@property (strong) IBOutlet NSButton *st2InstallButton;
@property (strong) IBOutlet NSButton *st3InstallButton;

@property (strong) IBOutlet NSProgressIndicator *st2ButtonLoading;
@property (strong) IBOutlet NSProgressIndicator *st3ButtonLoading;

+ (NSString *)nibName;
-(void)checkForPluginUpdates;
//-(IBAction)downloadPlugin:(id)sender;

@end
