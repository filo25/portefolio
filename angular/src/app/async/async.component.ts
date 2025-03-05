import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Observable, timer, of, throwError } from 'rxjs';
import { catchError, tap, map } from 'rxjs/operators';

let log = console.log;
let error = console.error;

// https://www.djamware.com/post/5da31946ae418d042e1aef1d/angular-8-tutorial-observable-and-rxjs-examples
// https://stackoverflow.com/questions/53420747/fromevent-in-angular
// https://www.geeksforgeeks.org/how-to-create-observable-data-stream-using-fromevent-method-in-angularjs/

@Component({
  selector: 'app-async',
  imports: [
    CommonModule
  ],
  templateUrl: './async.component.html',
  styleUrl: './async.component.scss'
})
export class AsyncComponent implements OnInit, AfterViewInit {

  nums = new Array<number>()
  numsSource: Observable<number> = timer(1000, 2000)
  numsSubsc: any

  fruits = new Array<string>()
  fruitsBag = ['apple', 'orange', 'grape', 'cherry', 'lime', 'berry', 'grapefruit']
  fruitsSource: Observable<number> = timer(1000, 2000)
  fruitsSubsc: any
  fruitId = 0

  constructor() {

    this.numsSubsc = this.numsSource.subscribe(val => this.nums.push(val as number))
    this.fruitsSubsc = this.fruitsSource.subscribe(val => {
      this.fruits.push(this.fruitsBag[this.fruitId]);
      this.fruitId += 1
    })

  }

  ngOnInit() {

    setTimeout(() => {
      this.numsSubsc!.unsubscribe();
      this.fruitsSubsc!.unsubscribe();
    }, 14000)

  }

  fromEvent(target: HTMLInputElement, eventName: string) {
    return new Observable((observer) => {
      const handler = (e: unknown) => observer.next(e)

      target.addEventListener(eventName, handler)

      return () => {
        target.removeEventListener(eventName, handler)
      }
    });
  }

  ngAfterViewInit() {
    const ESC_KEY = 27
    const SPACE_KEY = 32

    const nameInput = document.getElementById('beep') as HTMLInputElement

    // KeyboardEvent | undefined
    this.fromEvent(nameInput, 'keydown').subscribe( (e) => {

      let _e = e as KeyboardEvent
      log(`keypress: ${_e.keyCode}`)

      if ( _e.keyCode == ESC_KEY ) {
        nameInput.value = '';
        log('got an escape')
      }
      else if ( _e.keyCode == SPACE_KEY ) {
        nameInput.value = 'scoobee';
        log('got a space')
      }

    });
  }

}

