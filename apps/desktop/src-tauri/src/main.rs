#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
use std::{io::{BufRead, BufReader}, process::{Child, Command, Stdio}, sync::{Mutex, mpsc}, time::Duration};
use tauri::{Manager, WebviewUrl, WebviewWindowBuilder};

struct Engine(Mutex<Option<Child>>);
impl Engine {
    fn stop(&self) {
        if let Some(mut child) = self.0.lock().unwrap().take() {
            let _ = child.kill();
            let _ = child.wait();
        }
    }
}
impl Drop for Engine {fn drop(&mut self){self.stop();}}

fn startup_error() {
    #[cfg(windows)] unsafe {
        #[link(name="user32")]
        extern "system" {fn MessageBoxW(window:*mut std::ffi::c_void,text:*const u16,title:*const u16,kind:u32)->i32;}
        let text:Vec<u16>="Color Studio no puede iniciar el motor local. Reinicia la aplicación o reinstala la beta. / Cannot start the local engine. Restart or reinstall the beta.".encode_utf16().chain(Some(0)).collect();
        let title:Vec<u16>="Color Studio Beta".encode_utf16().chain(Some(0)).collect();
        MessageBoxW(std::ptr::null_mut(),text.as_ptr(),title.as_ptr(),0x10);
    }
}

fn main() {
    // One writer for the private data directory; cookies are also host-scoped.
    #[cfg(windows)] let _instance = match Instance::acquire() {Some(value)=>value,None=>return};
    let application=tauri::Builder::default()
        .setup(|app| {
            let executable=std::env::current_exe()?.parent().unwrap().join("ColorEngine.exe");
            let mut command=Command::new(executable);
            command.arg("--parent").arg(std::process::id().to_string())
                .stdout(Stdio::piped()).stderr(Stdio::null());
            #[cfg(windows)] {
                use std::os::windows::process::CommandExt;
                command.creation_flags(0x08000000);
            }
            let mut child=command.spawn()?;
            let stdout=child.stdout.take().unwrap();
            let engine=Engine(Mutex::new(Some(child)));
            let (sender,receiver)=mpsc::channel();
            std::thread::spawn(move || {
                let mut line=String::new();
                let result=BufReader::new(stdout).read_line(&mut line).map(|_|line);
                let _=sender.send(result);
            });
            let line=match receiver.recv_timeout(Duration::from_secs(45)) {
                Ok(Ok(line))=>line,
                _=>{engine.stop();return Err("Local engine failed to start. Restart Color Studio.".into())}
            };
            let result:serde_json::Value=serde_json::from_str(&line)?;
            let port=result["port"].as_u64().filter(|p|*p>0&&*p<65536).ok_or("Invalid local engine port")?;
            let origin=format!("http://127.0.0.1:{port}");
            app.manage(engine);
            let allowed=origin.clone();
            WebviewWindowBuilder::new(app,"studio",WebviewUrl::External(origin.parse()?))
                .title("Color Studio · Technical Beta").inner_size(1440.0,960.0).min_inner_size(900.0,650.0)
                .on_navigation(move |url| url.as_str().starts_with(&(allowed.clone()+"/")) || url.scheme()=="blob")
                .build()?;
            Ok(())
        })
        .build(tauri::generate_context!());
    let application=match application {Ok(app)=>app,Err(_)=>{startup_error();return;}};
    application.run(|handle,event| {
        if matches!(event,tauri::RunEvent::Exit) {
            if let Some(engine)=handle.try_state::<Engine>() {engine.stop();}
        }
    });
}

#[cfg(windows)]
struct Instance(*mut std::ffi::c_void);
#[cfg(windows)]
impl Instance {
    fn acquire()->Option<Self> {unsafe {
        #[link(name="kernel32")]
        extern "system" {
            fn CreateMutexW(attributes:*mut std::ffi::c_void,owner:i32,name:*const u16)->*mut std::ffi::c_void;
            fn GetLastError()->u32;
            fn CloseHandle(handle:*mut std::ffi::c_void)->i32;
        }
        let name:Vec<u16>="Local\\ColorStudioTechnicalBetaSingleInstance".encode_utf16().chain(Some(0)).collect();
        let handle=CreateMutexW(std::ptr::null_mut(),0,name.as_ptr());
        if handle.is_null(){startup_error();return None}
        if GetLastError()==183 {CloseHandle(handle);return None}
        Some(Self(handle))
    }}
}
#[cfg(windows)]
impl Drop for Instance {fn drop(&mut self){unsafe {
    #[link(name="kernel32")]
    extern "system" {fn CloseHandle(handle:*mut std::ffi::c_void)->i32;}
    CloseHandle(self.0);
}}}
