import { Component, OnInit } from '@angular/core';
import { Ticker } from '../ticker.model';

@Component({
  selector: 'app-ticker-list',
  templateUrl: './ticker-list.component.html',
  styleUrls: ['./ticker-list.component.css']
})
export class TickerListComponent implements OnInit {
  tickerArr: Ticker[] = [
    new Ticker('TSLA', 'Tesla', 69420, 89),
    new Ticker('APPL', 'Apple', 10, 22), 
    new Ticker('MSFT', 'Microsoft', 70, 99)
  ];

  constructor() { }

  ngOnInit(): void {
  }

}
