import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { TickerListComponent } from './ticker-list/ticker-list.component';
import { TickerInfoComponent } from './ticker-info/ticker-info.component';

@NgModule({
  declarations: [
    AppComponent,
    TickerListComponent,
    TickerInfoComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
