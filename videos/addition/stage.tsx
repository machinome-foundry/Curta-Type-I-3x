// The film's template: the sets Curta and CurtaSplit and the element Sum,
// declared in movie.py beside this file. Every word on screen comes from the
// movie document (the sets' props, the element's props); the layout and the
// look are this file's and stage.css's.
import {Chrome, Slot, defineElement, defineSet} from 'videomaker/stage';
import type {ElementComponentProps, SetComponentProps} from 'videomaker/stage';
import type {CurtaProps, CurtaSplitProps, SumState} from 'videomaker/movie';
import './stage.css';

// The masthead: the series at the left in brass, the brand at the right,
// muted. Drawn in Chrome so it stays still and sharp above pictures and
// joins. No rule, no bar, no progress: where a viewer is in the film is the
// player's.
function Masthead({series, brand}: {series: string; brand: string}) {
  return (
    <Chrome>
      <div className="curta-series">{series}</div>
      <div className="curta-brand">{brand}</div>
    </Chrome>
  );
}

// The root set: the machine fills the page below the masthead; a headline
// column at the left for a title; a small plate at the lower right for the
// sum. The stage's box is the same height as the split's right container, so
// a reframe between them changes the width the Curta stands in, not its size.
function Curta({props}: SetComponentProps<CurtaProps>) {
  return (
    <div className="curta">
      <Masthead series={props.series} brand={props.brand}/>
      <Slot name="stage" className="curta-stage"/>
      <Slot name="headline" className="curta-headline"/>
      <Slot name="aside" className="curta-aside"/>
    </div>
  );
}

// Derived by composition: the same masthead, the source in a container at
// the left, the machine in the right half.
function CurtaSplit({props}: SetComponentProps<CurtaSplitProps>) {
  return (
    <div className="curta">
      <Masthead series={props.series} brand={props.brand}/>
      <Slot name="left" className="curta-left"/>
      <Slot name="right" className="curta-right"/>
    </div>
  );
}

// The sum as it forms: the rows of its `rows` prop up to the one a `light`
// action names, that row in brass; nothing while no row is lit.
type Row = {key: string; text: string};
function Sum({state}: ElementComponentProps<SumState>) {
  const lit = state.actions.find(action => action.action === 'light')?.params.row;
  const rows = state.props.rows as Row[];
  const through = rows.findIndex(row => row.key === lit);
  if (through < 0) return null;
  return (
    <ol className="sum">
      {rows.slice(0, through + 1).map(row => (
        <li key={row.key} className={row.key === lit ? 'sum-row sum-lit' : 'sum-row'}>{row.text}</li>
      ))}
    </ol>
  );
}

defineSet({kind: 'curta', slots: ['stage', 'headline', 'aside'], component: Curta});
defineSet({kind: 'curta-split', slots: ['left', 'right'], component: CurtaSplit});
defineElement({kind: 'sum', component: Sum});
