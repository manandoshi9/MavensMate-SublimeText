//
//  PluginViewsController.m
//  MavensMate
//
//  Created by Joseph on 3/30/13.
//  Copyright (c) 2013 Joseph. All rights reserved.
//

#import "PluginViewsController.h"

@implementation PluginViewsController 


- (void)setupToolbar{
    [self addView:self.sublimeText2View label:@"Sublime Text 2" image:[NSImage imageNamed:@"Sublime_Text_Logo"]];
    [self addView:self.sublimeText3View label:@"Sublime Text 3" image:[NSImage imageNamed:@"Sublime_Text_Logo"]];
    [self addView:self.futurePluginView label:@"Future Plugin" image:[NSImage imageNamed:@"MavensMateMenuBarIconHighlightedWhite"]];

    // Optional configuration settings.
    [self setCrossFade:[[NSUserDefaults standardUserDefaults] boolForKey:@"fade"]];
    [self setShiftSlowsAnimation:[[NSUserDefaults standardUserDefaults] boolForKey:@"shiftSlowsAnimation"]];
}

- (IBAction)showWindow:(id)sender{
    [super showWindow:sender];
    [self checkForPluginUpdates];
}

-(void)checkForPluginUpdates {
    [self.st2InstallButton setEnabled:0];
    [self.st3InstallButton setEnabled:0];
    [self.st2InstallButton setTitle:@""];
    [self.st3InstallButton setTitle:@""];

    [self.st2ButtonLoading setHidden:0];
    [self.st2ButtonLoading setHidden:0];
    [self.st2ButtonLoading startAnimation:self];
    [self.st3ButtonLoading startAnimation:self];
    
    [self performSelectorInBackground:@selector(checkPluginVersions) withObject:nil];
}

+ (NSString *)nibName{
    return @"PluginViews";
}

-(void) checkPluginVersions {
    
    NSString *mavensMateSublimeText2PluginPath = [@"~/Library/Application Support/Sublime Text 2/Packages/MavensMate" stringByExpandingTildeInPath];
    NSString *mavensMateSublimeText3PluginPath = [@"~/Library/Application Support/Sublime Text 3/Packages/MavensMate" stringByExpandingTildeInPath];

    NSFileManager *filemgr = [NSFileManager defaultManager];

    BOOL mavensMateSublimeText2PluginPathIsDirectory;
    BOOL mavensMateSublimeText3PluginPathIsDirectory;
    
    //check for Sublime Text 2 status
    BOOL mavensMateSublimeText2PluginPathExists = [filemgr fileExistsAtPath:mavensMateSublimeText2PluginPath isDirectory:&mavensMateSublimeText2PluginPathIsDirectory];
    if (mavensMateSublimeText2PluginPathExists && mavensMateSublimeText2PluginPathIsDirectory) {
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
        
        
        NSString *mavensMateSublimeText2PluginPackagesPath = [@"~/Library/Application Support/Sublime Text 2/Packages/MavensMate/packages.json" stringByExpandingTildeInPath];
        NSData* data = [NSData dataWithContentsOfFile:mavensMateSublimeText2PluginPackagesPath];
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
        
        //NSLog(@"LOCAL VERSION: %@", localVersion);
        //NSLog(@"SERVER VERSION: %@", serverVersion);
        
        if (localVersionInt < serverVersionInt) {
            [self setSublimeText2ButtonTitles:@"Update Plugin"];
        } else if (localVersionInt >= serverVersionInt) {
            [self setSublimeText2ButtonTitles:@"Reload Plugin"];
        } else {
            [self setSublimeText2ButtonTitles:@"Install Plugin"];
        }
    } else {
        [self setSublimeText2ButtonTitles:@"Install Plugin"];
    }
    
    //check for Sublime Text 3 status
    BOOL mavensMateSublimeText3PluginPathExists = [filemgr fileExistsAtPath:mavensMateSublimeText3PluginPath isDirectory:&mavensMateSublimeText3PluginPathIsDirectory];
    if (mavensMateSublimeText3PluginPathExists && mavensMateSublimeText3PluginPathIsDirectory) {
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
        
        
        NSString *mavensMateSublimeText2PluginPackagesPath = [@"~/Library/Application Support/Sublime Text 3/Packages/MavensMate/packages.json" stringByExpandingTildeInPath];
        NSData* data = [NSData dataWithContentsOfFile:mavensMateSublimeText2PluginPackagesPath];
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
            [self setSublimeText3ButtonTitles:@"Update Plugin"];
        } else if (localVersionInt >= serverVersionInt) {
            [self setSublimeText3ButtonTitles:@"Reload Plugin"];
        } else {
            [self setSublimeText3ButtonTitles:@"Install Plugin"];
        }
    } else {
        [self setSublimeText3ButtonTitles:@"Install Plugin"];
    }
    
}

-(void)setSublimeText2ButtonTitles:(NSString*)title {
    [self.st2InstallButton setEnabled:1];
    [self.st2ButtonLoading setHidden:1];
    [self.st2InstallButton setTitle:title];
}

-(void)setSublimeText3ButtonTitles:(NSString*)title {
    [self.st3InstallButton setEnabled:1];
    [self.st3ButtonLoading setHidden:1];
    [self.st3InstallButton setTitle:title];
}
    
-(IBAction)downloadPluginReceiver:(id)sender {
    NSString *identifier = [(NSButton *)sender identifier];
    NSLog(@"User clicked %@", identifier);    
    if(!_loadingController) {
        _loadingController = [[LoadingController alloc] init];
	}
    _alertController = [[AlertController alloc] init];
    [_loadingController show];
    [[_loadingController window] makeKeyAndOrderFront:nil];
    [[NSApplication sharedApplication] arrangeInFront:nil];
    
    NSDictionary * args = [NSDictionary dictionaryWithObjectsAndKeys: identifier, @"identifier", nil];
    [self performSelectorInBackground:@selector(downloadAndInstallPluginWrapper:) withObject:args];
}

- (void)downloadAndInstallPluginWrapper:(NSDictionary *)args {
    NSString* identifier = [args objectForKey:@"identifier"];
    [self downloadAndInstallPlugin:identifier];
}

-(void) hideLoading {
    [_loadingController hide];
}

-(void) showSuccessAlert {
    [_alertController show];
    [[_alertController window] makeKeyAndOrderFront:nil];
    [[NSApplication sharedApplication] arrangeInFront:nil];
}

-(void) downloadAndInstallPlugin:(NSString*)identifier {
    if (![identifier isEqual: @"st2InstallButton"] && ![identifier isEqual: @"st3InstallButton"]) {
        [self hideLoading];
        [_alertController showWithMessage:@"Unsupported plugin requested"];
        [[_alertController window] makeKeyAndOrderFront:nil];
        [[NSApplication sharedApplication] arrangeInFront:nil];
        return;
    }
    
    NSError *error;
    
    NSString* sublimeTextPackagesPath;
    NSString* mavensMateSublimeTextPluginPath;
    NSString* mavensMateSublimeTextPluginPathLegacy;

    if ([identifier isEqual: @"st2InstallButton"]) {
        sublimeTextPackagesPath = [@"~/Library/Application Support/Sublime Text 2/Packages" stringByExpandingTildeInPath];
        mavensMateSublimeTextPluginPath = [@"~/Library/Application Support/Sublime Text 2/Packages/MavensMate" stringByExpandingTildeInPath];
        mavensMateSublimeTextPluginPathLegacy = [@"~/Library/Application Support/Sublime Text 2/Packages/MavensMate-SublimeText-2.0" stringByExpandingTildeInPath];
    } else if ([identifier isEqual: @"st3InstallButton"]) {
        sublimeTextPackagesPath = [@"~/Library/Application Support/Sublime Text 3/Packages" stringByExpandingTildeInPath];
        mavensMateSublimeTextPluginPath = [@"~/Library/Application Support/Sublime Text 3/Packages/MavensMate" stringByExpandingTildeInPath];
        mavensMateSublimeTextPluginPathLegacy = [@"~/Library/Application Support/Sublime Text 3/Packages/MavensMate-SublimeText-2.0" stringByExpandingTildeInPath];
    }
    
    NSFileManager *filemgr;
    filemgr = [NSFileManager defaultManager];
    
    BOOL isDir;
    BOOL fileExists = [filemgr fileExistsAtPath:sublimeTextPackagesPath isDirectory:&isDir];
    
    if (fileExists == false && isDir == false) {
        [self hideLoading];
        [_alertController showWithMessage:@"The requested directory does not exist. This usually means you do not have Sublime Text installed."];
        [[_alertController window] makeKeyAndOrderFront:nil];
        [[NSApplication sharedApplication] arrangeInFront:nil];
        return;
    }
        
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
        if ([filemgr removeItemAtPath:mavensMateSublimeTextPluginPath error:&error] != YES)
            NSLog(@"Unable to remove MavensMate from packages path: %@", [error localizedDescription]);
        
        if ([filemgr removeItemAtPath:mavensMateSublimeTextPluginPathLegacy error:&error] != YES)
            NSLog(@"Could not find MavensMate-SublimeText-2.0 in packages: %@", [error localizedDescription]);
        
        //move fresh installation to packages path
        NSString *origin = [NSTemporaryDirectory() stringByAppendingString:@"MavensMate-SublimeText-2.0"];
        
        //clean up tmp directory
        if ([filemgr moveItemAtPath:origin toPath:mavensMateSublimeTextPluginPath error:&error] != YES)
            NSLog(@"Unable to move file: %@", [error localizedDescription]);
        
        [self performSelectorOnMainThread:@selector(hideLoading) withObject:nil waitUntilDone:NO];
        [self performSelectorInBackground:@selector(checkPluginVersions) withObject:nil];
        [self showSuccessAlert];
    }
}


@end
