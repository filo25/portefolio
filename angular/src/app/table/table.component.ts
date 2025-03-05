import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

let log = console.log;

type Entry = {
  name: string;
  occupation: string | undefined;
};

@Component({
  selector: 'app-table',
  imports: [CommonModule],
  templateUrl: './table.component.html',
  styleUrl: './table.component.scss'
})
export class TableComponent {

  entries: Entry[] = []

  constructor() {

  }

  add() {
    this.entries.push({name: "beep", occupation: "bap"})
    this.entries.push({name: "dom", occupation: "da"})

    log(this.entries.length);
  }

  pop() {
    this.entries.pop()
  }

  boop() {

    let M = new Map<string, string>([
      ["John Wick", "hitman"],
      ["Road Runner", "delivery bird"]
    ]);

    /*
    for ( let k in M.keys() )
    {
      let e: Entry = {name: k, occupation: M.get(k)}
      this.entries.push(e)
    }
    */

    //log(M.size);

    M.forEach( (v, k) => {
      log(`${k}: ${v}`)
    });
  }

}
