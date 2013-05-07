//
//  PluginsController.m
//  MavensMate
//
//  Created by Joseph on 3/22/13.
//  Copyright (c) 2013 Joseph. All rights reserved.
//

#import "PluginsController.h"

@implementation PluginsController

@synthesize loadingController = _loadingController;
@synthesize alertController = _alertController;
@synthesize sublimeTextInstallButton = _sublimeTextInstallButton;
@synthesize sublimeTextButtonProgressIndicator = _sublimeTextButtonProgressIndicator;
@synthesize sublimeTextBetaFlag = _sublimeTextBetaFlag;

@synthesize foobarbat = _foobarbat;


-(PluginsController*)init {
    self = [[PluginsController alloc] initWithWindowNibName:@"Plugins"];
    [self.window setDelegate:self];
    [self.window setLevel:kCGMainMenuWindowLevel-3];
    //[self.window setCollectionBehavior:NSWindowCollectionBehaviorStationary|NSWindowCollectionBehaviorCanJoinAllSpaces|NSWindowCollectionBehaviorFullScreenAuxiliary];
    [_sublimeTextButtonProgressIndicator startAnimation:self];
    self = [super init];
    if (self) {
        //init code here...
    }
    return self;
}

- (void)windowDidLoad {
    //[_sublimeTextInstallButton setTitle:@"ffdsdffdfd"];
    //need to run a check here to determine the server version vs installed version of plugin(s)    
    [_sublimeTextInstallButton setEnabled:0];
    [self performSelectorInBackground:@selector(checkPluginVersions) withObject:nil];
}

-(void)setSublimeTextButtonTitle:(NSString*)title {
    [_sublimeTextInstallButton setEnabled:1];
    [_sublimeTextButtonProgressIndicator setHidden:1];
    [_sublimeTextInstallButton setTitle:title];
}

- (void)windowWillLoad {
    [_sublimeTextButtonProgressIndicator setHidden:0];
}

-(void) checkPluginVersions {
    
    NSString *stPackagesPath = [@"~/Library/Application Support/Sublime Text 2/Packages/MavensMate" stringByExpandingTildeInPath];
    
    BOOL isDir;
    NSFileManager *filemgr = [NSFileManager defaultManager];
    BOOL fileExists = [filemgr fileExistsAtPath:stPackagesPath isDirectory:&isDir];
    if (fileExists && isDir) {
        //NSURLRequest *request = [NSURLRequest requestWithURL:[NSURL URLWithString:@"https://raw.github.com/joeferraro/MavensMate-SublimeText/master/packages.json"]];
        NSURLRequest *request = [NSURLRequest requestWithURL:[NSURL URLWithString:@"https://raw.github.com/joeferraro/MavensMate-SublimeText/2.0/packages.json"]];
        NSData *response = [NSURLConnection sendSynchronousRequest:request returningResponse:nil error:nil];
        
        NSError *jsonParsingError = nil;
        NSDictionary *sublimeTextPluginServerVersion = [NSJSONSerialization JSONObjectWithData:response options:NSJSONReadingMutableContainers error:&jsonParsingError];
                
        NSArray *packageListing = [sublimeTextPluginServerVersion objectForKey:@"packages"];
        NSDictionary *mainPackage = [packageListing objectAtIndex:0];
        NSDictionary *platforms = [mainPackage objectForKey:@"platforms"];
        NSDictionary *osxInfo = [[platforms objectForKey:@"osx"] objectAtIndex:0];
        NSString *serverVersion = [osxInfo objectForKey:@"version"];
        
        
        NSString *sublimeTextMavensMatePackagesPath = [@"~/Library/Application Support/Sublime Text 2/Packages/MavensMate/packages.json" stringByExpandingTildeInPath];
        NSData* data = [NSData dataWithContentsOfFile:sublimeTextMavensMatePackagesPath];
        NSDictionary *sublimeTextLocalPackagesData = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingMutableContainers error:&jsonParsingError];
        
        packageListing = [sublimeTextLocalPackagesData objectForKey:@"packages"];
        mainPackage = [packageListing objectAtIndex:0];
        platforms = [mainPackage objectForKey:@"platforms"];
        osxInfo = [[platforms objectForKey:@"osx"] objectAtIndex:0];
        NSString *localVersion = [osxInfo objectForKey:@"version"];
        
        localVersion = [localVersion stringByReplacingOccurrencesOfString:@"." withString:@""];
        serverVersion = [serverVersion stringByReplacingOccurrencesOfString:@"." withString:@""];
        
        NSInteger localVersionInt = [localVersion intValue];
        NSInteger serverVersionInt = [serverVersion intValue];
        
        NSLog(@"LOCAL VERSION: %@", localVersion);
        NSLog(@"SERVER VERSION: %@", serverVersion);
        
        if (localVersionInt < serverVersionInt) {
            [self setSublimeTextButtonTitle:@"Update Plugin"];
        } else if (localVersionInt >= serverVersionInt) {
            [self setSublimeTextButtonTitle:@"Reload Plugin"];
        } else {
            [self setSublimeTextButtonTitle:@"Install Plugin"];
        }
    } else {
        [self setSublimeTextButtonTitle:@"Install Plugin"];
    }
}

//directs user to sublime text github page to download
-(IBAction) downloadSublimeTextPlugin:(id)sender {
    if(!_loadingController) {
        _loadingController = [[LoadingController alloc] init];
	}
    //if(!_alertController) {
        _alertController = [[AlertController alloc] init];
	//}
    [_loadingController show];
    [[_loadingController window] makeKeyAndOrderFront:nil];
    [[NSApplication sharedApplication] arrangeInFront:nil];
    
    [self performSelectorInBackground:@selector(downloadAndInstallSublimeTextPlugin) withObject:nil];
}

-(void) hideLoading {
    [_loadingController hide];
}

-(void) showSuccessAlert {
    //[self performSelectorOnMainThread:@selector(hideLoading) withObject:nil waitUntilDone:NO];
    [_alertController show];
    [[_alertController window] makeKeyAndOrderFront:nil];
    [[NSApplication sharedApplication] arrangeInFront:nil];

}

-(void) downloadAndInstallSublimeTextPlugin {
    NSError *error;
    
    NSString* stPackagesPath;
    stPackagesPath = [@"~/Library/Application Support/Sublime Text 2/Packages/MavensMate" stringByExpandingTildeInPath];
    
    NSString* stPackagesPathLegacy;
    stPackagesPathLegacy = [@"~/Library/Application Support/Sublime Text 2/Packages/MavensMate-SublimeText-2.0" stringByExpandingTildeInPath];
    
    NSFileManager *filemgr;
    filemgr = [NSFileManager defaultManager];
    
    NSString *filePath = [NSTemporaryDirectory() stringByAppendingPathComponent:@"mavensmate.zip"];
    //clean up tmp directory
    if ([filemgr removeItemAtPath:filePath error:&error] != YES)
        NSLog(@"Unable to remove zip from tmp path: %@", [error localizedDescription]);
    
    //download latest version
    NSString *myurl = @"https://github.com/joeferraro/MavensMate-SublimeText/archive/2.0.zip";
    NSData* data = [NSData dataWithContentsOfURL:[NSURL URLWithString:myurl]];
    
    if (data == nil) {
        NSLog(@"Install/Update likely failed");
        [self performSelectorOnMainThread:@selector(hideLoading) withObject:nil waitUntilDone:NO];
        NSString *message = @"Update failed. There may be a problem with your internet connection or Github may be experiencing issues. Please try again later.";
        [_alertController showWithMessage:message];
        [[_alertController window] makeKeyAndOrderFront:nil];
        [[NSApplication sharedApplication] arrangeInFront:nil];
    } else {
        [data writeToFile:filePath atomically:YES];
        
        //change directory to tmp (where file is downloaded)
        if ([filemgr changeCurrentDirectoryPath: NSTemporaryDirectory()] == NO)
            NSLog (@"Cannot change directory.");
        
        //unzip the file
        NSString *path = @"/usr/bin/unzip";
        NSArray *args = [NSArray arrayWithObjects:@"mavensmate.zip", nil];
        [[NSTask launchedTaskWithLaunchPath:path arguments:args] waitUntilExit];
        
        //clean up existing installation
        if ([filemgr removeItemAtPath:stPackagesPath error:&error] != YES)
            NSLog(@"Unable to remove MavensMate from packages path: %@", [error localizedDescription]);
        
        if ([filemgr removeItemAtPath:stPackagesPathLegacy error:&error] != YES)
            NSLog(@"Could not find MavensMate-SublimeText-2.0 in packages: %@", [error localizedDescription]);
        
        //move fresh installation to packages path
        NSString *origin = [NSTemporaryDirectory() stringByAppendingString:@"MavensMate-SublimeText-2.0"];
        //NSLog(origin);
        //NSLog(stPackagesPath);
        
        //clean up tmp directory
        if ([filemgr moveItemAtPath:origin toPath:stPackagesPath error:&error] != YES)
            NSLog(@"Unable to move file: %@", [error localizedDescription]);
        
        [self performSelectorOnMainThread:@selector(hideLoading) withObject:nil waitUntilDone:NO];
        [self showSuccessAlert];
    }
}



@end
