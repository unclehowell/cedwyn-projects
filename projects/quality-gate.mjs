import fs from "node:fs";
const read = (p) => fs.readFileSync(new URL(p, import.meta.url), "utf8");
const errors = [];
const ok = (condition, message) => { if (!condition) errors.push(message); };
let programme;
try { programme = JSON.parse(read("./public/data/programme.json")); }
catch (error) { errors.push("programme.json must parse: " + error.message); }
try { JSON.parse(read("./public/data/hubspot-snapshot.json")); }
catch (error) { errors.push("hubspot-snapshot.json must parse: " + error.message); }
const home=read("./public/index.html");
const pid=read("./public/estate/pid/index.html");
const stages=read("./public/estate/stage-plans/index.html");
const controls=read("./public/governance/continuity-controls/index.html");
const snapshot=read("./public/data/hubspot-snapshot.json");
const snowball=[...home.matchAll(/<h[23][^>]*>Cedwyn Snowball — programme-wide operating flywheel<\/h[23]>/g)];
ok(snowball.length===1,"home page must have exactly one top-level Snowball heading");
const ids=[...home.matchAll(/\bid=\"([^\"]+)\"/g)].map(m=>m[1]);
ok(new Set(ids).size===ids.length,"home page contains duplicate HTML ids");
ok(home.includes("Data freshness")&&home.includes("historical (30 October 2026)"),"home page must disclose historic queue/portfolio data");
ok(!home.includes("P1 can begin")&&!home.includes("P3 can begin")&&!home.includes("P2 continues"),"home page must not reuse superseded P1/P2/P3 labels");
ok(home.includes('href="data/hubspot-snapshot.json"'),"snapshot link must be relative to Project Office base path");
ok(home.includes("/governance/continuity-controls/"),"home page must link continuity controls");
ok(pid.includes("PRINCE2 Project Management (Version 7)"),"PID must use current PeopleCert method name");
ok(pid.includes("not a substitute for an appointed, independent Project Assurance role"),"PID must disclose that independent Project Assurance is not appointed");
ok(!pid.includes("Every 6 hours (research flywheel)"),"PID must not claim unsupported six-hour cadence");
ok(pid.includes("no autonomous external sending"),"PID must state outbound communication gate");
ok(stages.includes("baseline finish 1 Nov 2026 passed")&&stages.includes("S2 stage-entry approval"),"stage plan must expose missed baseline and stage-exit gate");
ok(controls.includes("Candidate is not a finding")&&controls.includes("external report"),"continuity controls must preserve the allegation/reporting stop gate");
ok(snapshot.includes("30 October 2026"),"historic snapshot must retain its true as-of date");
if(errors.length){console.error("PROJECT OFFICE INTEGRITY GATE FAILED");for(const e of errors)console.error(" - "+e);process.exitCode=1;}
else console.log("PROJECT OFFICE INTEGRITY GATE PASSED");
