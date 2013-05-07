//
//  DragAndDropStatusMenuView.m
//  MavensMate
//
//  Created by Joseph on 3/22/13.
//  Copyright (c) 2013 Joseph. All rights reserved.
//


#import "DragAndDropStatusMenuView.h"

@interface DragAndDropStatusMenuView ()

-(void)mouseDown:(NSEvent *)theEvent;
-(void)menuWillOpen:(NSMenu *)menu;
-(void)menuDidClose:(NSMenu *)menu;
-(void)drawRect:(NSRect)dirtyRect;
-(NSDragOperation)draggingEntered:(id<NSDraggingInfo>)sender;

@end

@implementation DragAndDropStatusMenuView

@synthesize statusItem = _statusItem;

- (id)initWithFrame:(NSRect)frame {
    self = [super initWithFrame:frame];
    if (self) {
		_statusItem = nil;
		_menu = nil;
		_isMenuVisible = NO;
        [self registerForDraggedTypes:[NSArray arrayWithObjects: NSFilenamesPboardType, nil]];
    }
    return self;
}


-(void)drawRect:(NSRect)dirtyRect {
    // Draw status bar background, highlighted (blue) if menu is showing
    [_statusItem drawStatusBarBackgroundInRect:[self bounds]
                                 withHighlight:_isMenuVisible];
	
    // Draw icon itself, either base or highlighted version
    NSRect rect = {-2,-2,21,21};
    if (_isMenuVisible) {
        [[NSImage imageNamed:@"MavensMateMenuBarIconHighlightedWhite"] drawInRect:dirtyRect
                                                            fromRect:rect
                                                           operation:NSCompositeSourceOver
                                                            fraction:1];
    } else {
        [[NSImage imageNamed:@"MavensMateMenuBarIconNew"] drawInRect:dirtyRect
                                                            fromRect:rect
                                                           operation:NSCompositeSourceOver
                                                            fraction:1];
    }
}

-(void)mouseDown:(NSEvent *)theEvent {
    //assert(_statusItem);
    [[self menu] setDelegate:self];
	[_statusItem popUpStatusItemMenu:[self menu]];
    //[self setNeedsDisplay:YES];
}

- (void)menuWillOpen:(NSMenu *)menu {
    _isMenuVisible = YES;
    [self setNeedsDisplay:YES];
}

- (void)menuDidClose:(NSMenu *)menu {
    _isMenuVisible = NO;
    [self.menu setDelegate:nil];
    [self setNeedsDisplay:YES];
}

- (NSDragOperation)draggingEntered:(id<NSDraggingInfo>)sender{
    return NSDragOperationCopy;
}

- (BOOL)performDragOperation:(id <NSDraggingInfo>)sender {
    NSPasteboard *pboard;
    //NSDragOperation sourceDragMask;
	
    //sourceDragMask = [sender draggingSourceOperationMask];
    pboard = [sender draggingPasteboard];
    if ( [[pboard types] containsObject:NSFilenamesPboardType] ) {
        NSArray *files = [pboard propertyListForType:NSFilenamesPboardType];
        NSLog(@"DRAG OPERATION: %@", files);
        NSLog(@"DRAG LENGTH: %lu", [files count]);
        if ([files count] == 1) {
            NSLog(@"SUCCESSFUL DRAG OPERATION: %@", files);
            __block NSMutableArray *urls = [[NSMutableArray alloc] init];
            [files enumerateObjectsUsingBlock:^(id obj, NSUInteger idx, BOOL *stop) {
                [urls addObject:[NSURL fileURLWithPath:obj]];
            }];
            //		PRYVFileController *fileController = [[PRYVFileController alloc] init];
            //		[fileController pryvFiles:[urls autorelease]
            //						 withTags:[[[NSSet alloc] init] autorelease]
            //					andFolderName:@""];
            //		[fileController release];
        }
    }
    return YES;
}


@end

